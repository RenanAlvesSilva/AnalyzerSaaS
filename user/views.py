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