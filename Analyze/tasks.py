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
            analyze_resume = resume_ai.Analyzer_gemini(
                resume_text=extracted,
                area_atuacao=instance.area_atuacao,
                nivel_senioridade=instance.nivel_senioridade,
                palavras_chave=instance.palavras_chave or [],
                nome_vaga=instance.nome_vaga
            )
            instance.resume_analyze = analyze_resume
            print("Extraído com sucesso:", bool(extracted))
            print("Palavras-chave:", instance.palavras_chave)
            print("Nome da vaga:", instance.nome_vaga)

        
        instance.save()
        
    except Analyzer.DoesNotExist:
        print(f"Analyse com ID {analyzer_id} não encontrado.")
    except Exception as e:
        print(f"Erro ao processar a análise AI para o ID {analyzer_id}: {str(e)}")
            
    