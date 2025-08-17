from rest_framework import viewsets
from .serializers import AnalyzerSerializer
from .models import Analyzer
from .tasks import analyze_ai_task
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status



class AnalyzerViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyzerSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Analyzer.objects.filter(usuario=self.request.user)
    
     
    def create(self, request,*args, **kwargs):
        area_atuacao = request.data.get('area_atuacao', None)
        nivel_senioridade = request.data.get('nivel_senioridade', None)
        palavras_chave = request.data.getlist('palavras_chave')
        nome_vaga = request.data.get('nome_vaga')
        arquivos = request.FILES.getlist('file')
        
        dados = []
        for arquivo in arquivos:
            dados.append({
                'file': arquivo,
                'area_atuacao': area_atuacao,
                'nivel_senioridade': nivel_senioridade,
                'palavras_chave': palavras_chave,
                'nome_vaga': nome_vaga
            })
         
        serializer = self.get_serializer(data=dados, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_bulk_create(self, serializer):
        instances = serializer.save(usuario=self.request.user)
        for instance in instances:
           analyze_ai_task.delay(instance.id)
          