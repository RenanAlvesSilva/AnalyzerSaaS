from rest_framework import serializers
from .models import Analyzer


class AnalyzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyzer
        fields = '__all__'
        
    def validate_files(self, files):
        for f in files:
            if f.file.endswith('.pdf'):
                return serializers.ValidationError("Apenas arquivos PDF podem ser enviados.")

        return files