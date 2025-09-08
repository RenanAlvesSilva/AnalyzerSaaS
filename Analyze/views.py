from rest_framework import viewsets
from .serializers import AnalyzerSerializer
from .models import Analyzer
from .tasks import analyze_ai_task
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework import status

class AnalyzerViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyzerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Analyzer.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
     
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
        response_data =self.perform_bulk_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_bulk_create(self, serializer):
    
        instances = serializer.save(
            usuario=self.request.user,
            status='NA_FILA'
        )
        tasks_info = []
        for instance in instances:
            task = analyze_ai_task.delay(instance.id)
            tasks_info.append({
                'analyzer_id': instance.id,
                'task_id': task.id
            })
        return tasks_info
            
            
class TaskStatusView(APIView):
    queryset = Analyzer.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request,task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)
        result = {
            'task_id': task_id,
            'status': task_result.status,
            'result': task_result.result if task_result.ready() else None
        }
        
        return Response(result, status=status.HTTP_200_OK)
          