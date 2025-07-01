from google import genai
from decouple import config




class AnalyzerAI:
    def Analyzer_gemini(self, pdf_path):
        try:
            cliente = genai.Client(api_key=config("GEMINI_API_KEY"))
            prompt = """
                    Você é uma recrutadora técnica especialista em Desenvolvimento de Software, Engenharia de Dados, DevOps e Automação. Vou te fornecer o texto bruto de um currículo. Analise detalhadamente e responda seguindo os tópicos abaixo:

                    1. Resumo geral do perfil (área de atuação percebida + nível de senioridade: Estagiário, Júnior, Pleno ou Sênior)
                    2. Pontos fortes do currículo
                    3. Pontos de melhoria
                    4. Sugestões de stacks ou tecnologias para aprender, de acordo com o nível atual da pessoa
                    5. Dicas para melhorar o currículo (estrutura, clareza, conteúdo)
                    6. Sugestões de cargos adequados ao perfil
                    7. Caso faltem informações importantes, avise ao final de forma gentil e dê orientações para complementar

                    Importante: Se o candidato for estagiário ou iniciante, adapte o tom para ser mais construtivo, realista e incentivador.

                    Após este prompt, te enviarei apenas o texto do currículo.
            """
            
            
            response = cliente.models.generate_content(
                model='gemini-2.5-flash', contents= [prompt, pdf_path],
                
            )
            return response.text

        except Exception as e:
            return f"An error occurred: {str(e)}"


