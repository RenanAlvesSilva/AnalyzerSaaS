from rest_framework import viewsets
from .serializers import AnalyzerSerializer
from .models import Analyzer
from .tasks import analyze_ai_task
from rest_framework.permissions import IsAuthenticated



class AnalyzerViewSet(viewsets.ModelViewSet):
     queryset = Analyzer.objects.all()
     serializer_class = AnalyzerSerializer
     permission_classes = [IsAuthenticated]
     def perform_create(self, serializer):
         instance = serializer.save()
         analyze_ai_task.delay(instance.id)
          