from django.db import models
from django.conf import settings
   

class Analyzer(models.Model):
    STATUS_CHOICE = [
        ('NA_FILA', 'Na Fila'),
        ('PROCESSANDO', 'Processando'),
        ('CONCLUIDO', 'Concluído'),
        ('FALHA', 'Falha'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuarios', blank=False, null=False)
    file = models.FileField(upload_to='analisados/')
    extracted_text = models.TextField(blank=True, null=True)
    resume_analyze = models.TextField(blank=True, null=True)
    area_atuacao = models.CharField(max_length=255, blank=True, null=True)
    nivel_senioridade = models.CharField(max_length=255, blank=True, null=True)
    palavras_chave = models.JSONField(blank=True, null=True)
    nome_vaga = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='NA_FILA')
    def __str__(self):
        return f'{self.file.name} - {self.id}'
    