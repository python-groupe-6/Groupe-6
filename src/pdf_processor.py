import pypdf
import re
from docx import Document
import io

class PDFProcessor:
    """
    Renamed logically to DocumentProcessor internally.
    Handles extraction from PDF, DOCX, and TXT.
    """
    def __init__(self, file_path=None):
        self.file_path = file_path

    def extract_text(self, uploaded_file=None):
        """
        Extracts text from various file formats.
        """
        if not uploaded_file and not self.file_path:
            return "No file provided"

        file_to_process = uploaded_file if uploaded_file else self.file_path
        filename = uploaded_file.name if uploaded_file else self.file_path

        try:
            if filename.lower().endswith('.pdf'):
                return self._extract_from_pdf(file_to_process)
            elif filename.lower().endswith('.docx'):
                return self._extract_from_docx(file_to_process)
            elif filename.lower().endswith('.txt'):
                return self._extract_from_txt(file_to_process)
            else:
                return "Format de fichier non supporté. Utilisez PDF, DOCX ou TXT."
        except Exception as e:
            return f"Erreur lors de l'extraction : {str(e)}"

    def _extract_from_pdf(self, file):
        text = ""
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return self.clean_text(text)

    def _extract_from_docx(self, file):
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return self.clean_text(text)

    def _extract_from_txt(self, file):
        if isinstance(file, str):
            with open(file, 'r', encoding='utf-8') as f:
                return self.clean_text(f.read())
        else:
            return self.clean_text(file.read().decode('utf-8'))

    def clean_text(self, text):
        """
        Cleans the extracted text.
        """
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        # Remove extra spaces
        text = re.sub(r' +', ' ', text)
        return text.strip()
