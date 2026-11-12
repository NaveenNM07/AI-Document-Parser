import fitz  # PyMuPDF
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts raw text content from a given PDF file path.

    Args:
        pdf_path (str): Path to the target PDF file.

    Returns:
        str: Cleaned extracted text from all pages.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found at path: {pdf_path}")

    extracted_text = []

    # Open PDF document
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            if text.strip():
                extracted_text.append(f"--- Page {page_num + 1} ---\n{text}")

    full_text = "\n\n".join(extracted_text)

    if not full_text.strip():
        return "WARNING: No readable text found in document. (The file might be a scanned image)."

    return full_text


if __name__ == "__main__":
    # Quick standalone test execution
    print("PDF Extractor module loaded successfully.")