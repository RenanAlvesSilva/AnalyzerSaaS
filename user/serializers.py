from rest_framework import serializers
from .models import *
from .tasks import send_user_token_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password


class CostumerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostumerUser
        fields = ["id", "name", "last_name", "email", "password", "is_staff", "is_manager", "is_employee", "is_active"]
        extra_kwargs = {"password": {"write_only": True},
                        "is_activate": {"read_only": True},
                        "is_staff": {"read_only": True},
                        "is_manager": {"read_only": True},
                        "is_employee": {"read_only": True}
                        }
        
    def create(self,validated_data):
            
            password = validated_data.pop("password")
            user = CostumerUser(**validated_data)
            user.set_password(password)
            user.is_staff = False
            user.save()
            send_user_token_email(
                user.pk, 
                "Confirmação de Email", 
                "api/v1/confirm-email", 
                "Confirmação de conta",
                message_template="emails/message_email.txt")
            return user
        
    def validate_name(self, value):
            
            if not value or len(value) < 3:
                raise serializers.ValidationError("O nome não posso ser um campo vazio ou menor que 3 caractéres.")
            if not all(part.isalpha() for part in value.split()):
                raise serializers.ValidationError("O nome deve conter apenas letras e espaços.")

            return value    
        
    def validate_last_name(self, value):
            
            if not value or len(value) < 3:
                raise serializers.ValidationError("O sobrenome não posso ser um campo vazio ou menor que 3 caractéres.")
            if not all(part.isalpha() for part in value.split()):
                raise serializers.ValidationError("O sobrenome deve conter apenas letras e espaços.")
            
            return value
        
    def validate_password(self,value):
            
            if not value or len(value) < 6:
                raise serializers.ValidationError("A senha não posso ser um campo vazio ou menor que 6 caractéres.")
            if not any( c in value for c in "!@#$%&*"):
                raise serializers.ValidationError("A senha deve conter pelo menos um caractére especial.")
            return value    
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        return CostumerUserSerializer.validate_password(self, value)
    
    def validate(self, data):
        user = self.context['user']
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("As senhas devem ser iguais.")
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("A senha atual está incorreta.")
        return data
    
    def save(self):
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, data):
        user = CostumerUser.objects.filter(email=data['email']).first()
        if not user:
            raise serializers.ValidationError("Nenhum usuário encontrado com este email.")
        data['user'] = user     
        return data
    
    def save(self):
        user = self.validated_data.get('user')
        if user:
            send_user_token_email(
                user.pk, 
                "Redefinição de Senha", 
                "api/v1/reset-password", 
                "Redefinição de senha",
                message_template="emails/message_email.txt"
            )
        else: 
            raise serializers.ValidationError("Nenhum usuário encontrado com este email.")
        return user
    

class ResetPasswordConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("As senhas devem ser iguais.")
        try:
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            user = CostumerUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CostumerUser.DoesNotExist):
            raise serializers.ValidationError("Usuário não encontrado.")
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Token inválido ou expirado.")
        
        
        data['user'] = user
        return data
    
    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    
    

