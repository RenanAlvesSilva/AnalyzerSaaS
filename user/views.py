from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.permissions import *


class CostumerUserViewSet(viewsets.ModelViewSet):
    queryset = CostumerUser.objects.all()
    serializer_class = CostumerUserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me (self, request):
        user = request.user
        serializer = CostumerUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CostumerUserSerializer
    def get(self, request, uidb64, token, format=None, *args , **kwargs):
        
        try:
           User = get_user_model()
           uid = urlsafe_base64_decode(uidb64).decode()
           user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CostumerUser.DoesNotExist):
            return Response({"error": "Usuário nao encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        if default_token_generator.check_token(user, token):
            user.activate_as_manager()
            return Response({"message": "Usuário ativado com sucesso!"}, status=status.HTTP_200_OK)
        else: return Response({"error": "Link de ativacao invalido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def patch (self, request , *args , **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data, context = {'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Senha alterada com sucesso!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Caso seja encontrado o email enviaremos instruções para redefinir a senha."}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            User = get_user_model()
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CostumerUser.DoesNotExist):
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        if default_token_generator.check_token(user, token):
            return Response({"message": "Token válido. Você pode redefinir sua senha."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Link de redefinição inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)
        


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordConfirmSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Senha redefinida com sucesso!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)