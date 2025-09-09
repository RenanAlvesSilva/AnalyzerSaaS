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
               Sua única tarefa é atuar como um classificador de currículos. Analise o texto do currículo fornecido com base nos critérios da vaga e nas palavras-chave.

                **Critérios da Vaga:**
                - Nome da Vaga: '{nome_vaga}'
                - Área de Atuação: '{area_atuacao}'
                - Nível de Senioridade: '{nivel_senioridade}'
                - Palavras-chave para buscar: {palavras_chave}

                **Instruções de Saída:**
                Responda **APENAS e SOMENTE** com um objeto JSON válido, sem saudações, explicações ou qualquer texto fora do JSON.
                O objeto JSON deve ter a seguinte estrutura e tipos de dados:
                {{
                "apto": boolean,
                "palavras_chave_encontradas": ["array de strings"],
                "justificativa": "string"
                }}

                **Regras para os campos:**
                1.  `apto`: Deve ser `true` se o candidato for minimamente qualificado e atender a pelo menos algumas das palavras-chave principais. Caso contrário, deve ser `false`.
                2.  `palavras_chave_encontradas`: Deve ser um array contendo **apenas** as palavras-chave da lista fornecida que foram encontradas no texto do currículo. Se nenhuma for encontrada, retorne um array vazio `[]`.
                3.  `justificativa`: Uma frase curta (máximo de 25 palavras) explicando o porquê da decisão no campo "apto".

                **Texto do Currículo para Análise:**
                ---
                {resume_text}
                ---
            """
            
            response = cliente.models.generate_content(
                model='gemini-2.5-flash', contents= [f"{prompt}\n\nCurrículo:\n{resume_text}"],
                
            )
            return response.text

        except TimeoutException:
            return "Ocorreu um erro ao processar a análise AI. A operação demorou demais e foi abortada."


