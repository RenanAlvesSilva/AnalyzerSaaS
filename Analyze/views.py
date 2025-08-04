from rest_framework import viewsets
from .serializers import AnalyzerSerializer
from .models import Analyzer
from .tasks import analyze_ai_task
from rest_framework.permissions import IsAuthenticated



class AnalyzerViewSet(viewsets.ModelViewSet):
    queryset = Analyzer.objects.all()
    serializer_class = AnalyzerSerializer
    permission_classes = [IsAuthenticated]
     
    def create(self, request, *args, **kwargs):
        arquivos = request.FILES.getlist('file')
        dados = [{'file': f} for f in arquivos]
         
        serializer = self.get_serializer(data=dados, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        headers = self,get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_bulk_create(self, serializer):
        instances = serializer.save()
        for instance in instances:
           analyze_ai_task.delay(instance.id)
          