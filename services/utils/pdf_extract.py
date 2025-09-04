import PyPDF2
from typing import IO

class ExtractPDF:
    def extract_text_from_pdf(self,pdf_stream: IO[bytes]):
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
                    
                return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ''

