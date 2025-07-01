from celery import shared_task
from .models import Analyzer
from services.ai.analyze_ai import AnalyzerAI
from services.utils.pdf_extract import ExtractPDF



@shared_task
def analyze_ai_task(analyzer_id):
    try:
        instance = Analyzer.objects.get(id = analyzer_id)
        
        extract_text = ExtractPDF()
        instance.file.open()
        instance.file.close()
        extracted = extract_text.extract_text_from_pdf(instance.file.path)
        instance.extracted_text = extracted
        
        
        if extracted:
            resume_ai = AnalyzerAI()
            analyze_resume = resume_ai.Analyzer_gemini(extracted)
            instance.resume_analyze = analyze_resume
        
        instance.save()
        
    except Analyzer.DoesNotExist:
        print(f"Analyse com ID {analyzer_id} não encontrado.")
    except Exception as e:
        print(f"Erro ao processar a análise AI para o ID {analyzer_id}: {str(e)}")
            
    