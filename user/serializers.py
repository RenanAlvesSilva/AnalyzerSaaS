from rest_framework import serializers
from .models import *

class CostumerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostumerUser
        fields = ["id", "name", "last_name", "email", "password", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}
        
    def create(self,validated_data):
            
            password = validated_data.pop("password")
            user = CostumerUser(**validated_data)
            user.set_password(password)
            user.is_staff = False
            user.save()
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
                raise serializers.ValidationError("O nome deve conter apenas letras e espaços.")

            return value
        
    def validate_password(self,value):
            
            if not value or len(value) < 6:
                raise serializers.ValidationError("A senha não posso ser um campo vazio ou menor que 6 caractéres.")
            if not any( c in value for c in "!@#$%&*"):
                raise serializers.ValidationError("A senha deve conter pelo menos um caractére especial.")
            return value    
                