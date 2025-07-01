from django.contrib import admin
from .models import Analyzer
from .tasks import analyze_ai_task

@admin.register(Analyzer)
class AnalyzerAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'extracted_text', 'resume_analyze')
    actions = ['analyze_ai_action']

    def analyze_ai_action(self, request, queryset):
        for instance in queryset:
            analyze_ai_task.delay(instance.id)  

        self.message_user(request, "Tasks de análise de IA enviadas para a fila Celery.")
    analyze_ai_action.short_description = "Rodar Análise de IA nos currículos selecionados"
