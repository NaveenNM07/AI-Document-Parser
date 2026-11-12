import os
from celery import Celery
from app.core.extractor import extract_text_from_pdf
from app.core.llm_parser import parse_text_with_llm

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "document_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="process_pdf_async")
def process_pdf_async(file_path: str, doc_type: str = "invoice"):
    """Background task to extract text and process AI parsing asynchronously."""
    try:
        raw_text = extract_text_from_pdf(file_path)
        parsed_json = parse_text_with_llm(raw_text, doc_type=doc_type)
        return {
            "status": "SUCCESS",
            "filename": os.path.basename(file_path),
            "document_type": doc_type,
            "parsed_data": parsed_json
        }
    except Exception as e:
        return {
            "status": "FAILURE",
            "filename": os.path.basename(file_path),
            "document_type": doc_type,
            "error": str(e)
        }