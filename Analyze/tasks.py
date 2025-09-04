from celery import shared_task
from .models import Analyzer
from services.ai.analyze_ai import AnalyzerAI
from services.utils.pdf_extract import ExtractPDF



@shared_task(bind=True) # Usar bind=True é uma boa prática para ter acesso ao contexto da task
def analyze_ai_task(self, analyzer_id):
    
    try:
        instance = Analyzer.objects.get(id=analyzer_id)
    except Analyzer.DoesNotExist:
        print(f"Analyzer com ID {analyzer_id} não encontrado. A tarefa não será executada.")
        return #

    try:
        #
        print(f"Iniciando extração para o Analyzer ID: {analyzer_id}")
        extract_service = ExtractPDF()
        
       
        with instance.file.open('rb') as pdf_file_stream:
            extracted_text = extract_service.extract_text_from_pdf(pdf_file_stream)

        if not extracted_text:
            print(f"Não foi possível extrair texto do arquivo para o Analyzer ID: {analyzer_id}. Encerrando.")
           
            instance.status = 'FALHA_EXTRACAO'
            instance.save()
            return

       
        instance.extracted_text = extracted_text
        
        instance.save(update_fields=['extracted_text'])
        print(f"Texto extraído e salvo para o Analyzer ID: {analyzer_id}")

        print(f"Enviando texto para análise de IA para o Analyzer ID: {analyzer_id}")
        resume_ai = AnalyzerAI()
        analysis_result = resume_ai.Analyzer_gemini(
            resume_text=extracted_text,
            area_atuacao=instance.area_atuacao,
            nivel_senioridade=instance.nivel_senioridade,
            palavras_chave=instance.palavras_chave or [], 
            nome_vaga=instance.nome_vaga
        )

        
        instance.resume_analyze = analysis_result
        instance.status = 'CONCLUIDO' 
        instance.save(update_fields=['resume_analyze'])
        print(f"Análise de IA concluída e salva para o Analyzer ID: {analyzer_id}")

        return f"Processamento do Analyzer {analyzer_id} concluído com sucesso."

    except Exception as e:
        print(f"Ocorreu um erro inesperado no processamento do Analyzer ID {analyzer_id}: {str(e)}")
        try:
            instance.status = 'ERRO'
            raise self.retry(exc=e, countdown=60) 
        except self.MaxRetriesExceededError:
            print(f"Máximo de tentativas atingido para o Analyzer ID {analyzer_id}.")

