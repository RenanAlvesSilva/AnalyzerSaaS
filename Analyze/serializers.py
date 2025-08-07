from rest_framework import serializers
from .models import Analyzer


class AnalyzerSerializer(serializers.ModelSerializer):
    area_atuacao = serializers.CharField(required=False, allow_blank=True)
    nivel_senioridade = serializers.CharField(required=False, allow_blank=True)
    nome_vaga= serializers.CharField(required=True, allow_blank=True)
    palavras_chave = serializers.ListField(child=serializers.CharField(), required=True)
    class Meta:
        model = Analyzer
        fields = ['file','extracted_text','resume_analyze','area_atuacao', 'nivel_senioridade', 'palavras_chave', 'nome_vaga']
        
    def validate(self, data):
        files = data.get('file')
        if files:
            if isinstance(files, list):
                for f in files:
                    if not f.name.endswith('.pdf'):
                        raise serializers.ValidationError("Apenas arquivos PDF podem ser enviados.")
            else:
                if not files.name.endswith('.pdf'):
                    raise serializers.ValidationError("O campo 'file' é obrigatório.")
                
            
        if not data.get('palavras_chave'):
            raise serializers.ValidationError({"Palavras_Chaves": "Esse campo é obrigatório.", "Nome_Vaga": "Esse campo é obrigatório."})
        if not data.get('nome_vaga'):
            raise serializers.ValidationError({"Nome_Vaga": "Esse campo é obrigatório."})
        return data