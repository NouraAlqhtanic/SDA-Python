import io
from pypdf import PdfReader


def extract_text_from_pdf(file_content: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_content))

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text.strip()