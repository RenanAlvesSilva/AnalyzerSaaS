from google import genai
from decouple import config
import threading


class TimeoutException(Exception): pass

def run_with_timeout(func, args=(), kwargs={}, timeout=15):
    result = [None]
    exc = [None]

    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exc[0] = e

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutException("Função demorou demais e foi abortada.")
    if exc[0]:
        raise exc[0]
    return result[0]

class AnalyzerAI:
    def Analyzer_gemini(self, resume_text, area_atuacao=None, nivel_senioridade=None, palavras_chave=None, nome_vaga=None):
        try:
            cliente = genai.Client(api_key=config("GEMINI_API_KEY"))
            prompt = f"""
                Você é um recrutador técnico responsável por selecionar candidatos para a vaga de {nome_vaga}, na área de {area_atuacao}.
                Vou te fornecer o texto bruto de um currículo. Analise detalhadamente e responda com base nos seguintes critérios:

                1. O candidato parece compatível com a vaga de {nome_vaga}? Considere a área de atuação percebida e o nível de senioridade estimado ({nivel_senioridade})
                2. Quais pontos fortes se destacam no currículo, especialmente nas características: {', '.join(palavras_chave)}
                3. Quais são os principais pontos de melhoria?
                4. Sugestões de tecnologias ou competências para desenvolver, visando maior aderência à vaga
                5. Cargos alternativos que possam ser mais adequados ao perfil
                6. Caso faltem informações importantes, indique de forma gentil o que pode ser complementado
                

                Importante: Considere sinônimos e variações das palavras-chave mencionadas. Se o candidato estiver em início de carreira, adote um tom incentivador e realista.

                Após este prompt, será enviado apenas o texto do currículo.

                Responda de forma clara e objectiva, resumindo ao máximo sua resposta para maior agilidade na análise.
            """
            
            response = cliente.models.generate_content(
                model='gemini-2.5-flash', contents= [f"{prompt}\n\nCurrículo:\n{resume_text}"],
                
            )
            return response.text

        except TimeoutException:
            return "Ocorreu um erro ao processar a análise AI. A operação demorou demais e foi abortada."


