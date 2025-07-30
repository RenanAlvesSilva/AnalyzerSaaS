from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

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
