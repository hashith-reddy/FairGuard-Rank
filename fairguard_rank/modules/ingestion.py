import io
import docx
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_stream: io.BytesIO) -> str:
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_docx(file_stream: io.BytesIO) -> str:
    doc = docx.Document(file_stream)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_resume(file_content: bytes, filename: str) -> str:
    file_stream = io.BytesIO(file_content)
    if filename.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_stream)
    elif filename.lower().endswith('.docx'):
        return extract_text_from_docx(file_stream)
    elif filename.lower().endswith('.txt'):
        return file_content.decode('utf-8', errors='ignore')
    else:
        raise ValueError("Unsupported file format. Please provide PDF, DOCX, or TXT.")
