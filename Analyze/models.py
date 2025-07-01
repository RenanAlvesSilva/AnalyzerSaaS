from django.db import models

class Analyzer(models.Model):
    
    file = models.FileField(upload_to='analisados/')
    extracted_text = models.TextField(blank=True, null=True)
    resume_analyze = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.file.name} - {self.id}'
    