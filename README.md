# AnalyzerAI

🚀 **AnalyzerAI** é uma aplicação para análise inteligente de currículos usando Inteligência Artificial. Desenvolvido com Django REST Framework, o sistema permite automatizar a leitura e análise de currículos em PDF, extraindo informações relevantes para otimizar o processo seletivo e ajuda para otimizar curriculo.

---

## 🧰 Tecnologias Utilizadas

- **Python 3.11+**
- **Django**
- **Django REST Framework (DRF)**
- **Celery** (para processamento assíncrono de tarefas)
- **RabbitMQ** (broker para Celery)
- **PyPDF2** (extração de texto de PDFs)
- **OpenAI API** (análise de conteúdo com IA)

---

## ⚙️ Funcionalidades

- Upload de currículos em PDF
- Extração automática de texto
- Análise do conteúdo via IA (OpenAI)
- Geração de análise detalhada (respostas automáticas sobre o candidato)
- Filas assíncronas para garantir escalabilidade e performance
- Retorno de status de análise em tempo real

---

## 💡 Como Executar o Projeto

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/RenanAlvesSilva/AnalyzerAI.git
cd Analyze

2️⃣ Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Configure variáveis de ambiente
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True

5️⃣ Migre o banco de dados
python manage.py migrate

6️⃣ Suba o servidor Django
python manage.py runserver

7️⃣ Com Docker aberto rode no CMD
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management

8️⃣ Inicie o Celery
Em outro terminal:
celery -A analyzer_ai worker -l info

🚀 Como Usar
Acesse a interface administrativa do Django (/admin) ou envie os currículos via API.

Faça upload de um PDF.

Aguarde a análise ser concluída (o status será atualizado).

Consulte os resultados na interface ou via endpoint de API.

📄 Endpoints Principais

POST /api/v1/analyzer/ — Upload de currículo para análise.

GET /api/v1/analyzer/ — Lista de análises.

GET api/schema/swagger-ui/ - Documentação da API em Swagger

POST /api/v1/analyzer/{id}/ — Inicia ou força a análise de um currículo específico.

🧑‍💻 Autor
Renan Alves

⭐ Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais informações.
