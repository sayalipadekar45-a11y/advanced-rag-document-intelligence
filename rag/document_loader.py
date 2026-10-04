import pymupdf
from pathlib import Path
from docx import Document


def extract_pdf_text(file_path):
    document = pymupdf.open(file_path)
    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()
    return pages


def extract_docx_text(file_path):
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    full_text = "\n".join(paragraphs)

    return [{
        "page": 1,
        "text": full_text
    }]


def extract_txt_text(file_path):
    text = Path(file_path).read_text(
        encoding="utf-8",
        errors="ignore"
    )

    return [{
        "page": 1,
        "text": text
    }]


def extract_text(file_path):
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)

    else:
        raise ValueError(
            "Unsupported file type. Supported: PDF, DOCX and TXT."
        )