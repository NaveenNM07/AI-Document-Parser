import os
import shutil
from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from app.core.extractor import extract_text_from_pdf
from app.core.llm_parser import parse_text_with_llm
from app.schemas.document import ExtractionResponse
from app.workers.celery_worker import process_pdf_async, celery_app

router = APIRouter(prefix="/api/v1", tags=["Document Processing"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/parse", response_model=ExtractionResponse)
async def parse_document_sync(
    file: UploadFile = File(...),
    doc_type: str = Query("invoice", description="Document type: 'invoice' or 'resume'")
):
    """Synchronous Endpoint: Uploads PDF and returns parsed JSON immediately."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        raw_text = extract_text_from_pdf(file_location)
        parsed_json = parse_text_with_llm(raw_text, doc_type=doc_type)

        return ExtractionResponse(
            filename=file.filename,
            document_type=doc_type,
            status="completed",
            parsed_data=parsed_json,
            error=None
        )

    except Exception as e:
        return ExtractionResponse(
            filename=file.filename,
            document_type=doc_type,
            status="failed",
            parsed_data={},
            error=str(e)
        )


@router.post("/parse-async")
async def parse_document_async(
    file: UploadFile = File(...),
    doc_type: str = Query("invoice", description="Document type: 'invoice' or 'resume'")
):
    """Asynchronous Endpoint: Dispatches parsing job to Celery worker and returns Task ID."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = process_pdf_async.delay(file_location, doc_type)
    return {"task_id": task.id, "status": "processing", "filename": file.filename}


@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """Check status or result of a background Celery task."""
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }