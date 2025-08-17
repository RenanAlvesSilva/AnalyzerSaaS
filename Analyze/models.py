from django.db import models
from django.conf import settings

class Analyzer(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuarios', blank=False, null=False)
    file = models.FileField(upload_to='analisados/')
    extracted_text = models.TextField(blank=True, null=True)
    resume_analyze = models.TextField(blank=True, null=True)
    area_atuacao = models.CharField(max_length=255, blank=True, null=True)
    nivel_senioridade = models.CharField(max_length=255, blank=True, null=True)
    palavras_chave = models.JSONField(blank=True, null=True)
    nome_vaga = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.file.name} - {self.id}'
    