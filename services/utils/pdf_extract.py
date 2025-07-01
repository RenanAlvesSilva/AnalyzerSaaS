import PyPDF2


class ExtractPDF:
    def extract_text_from_pdf(self,pdf_path):
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text() or ''
                    
                return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ''

