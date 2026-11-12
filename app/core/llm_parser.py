import json
import os
import requests
from app.schemas.document import InvoiceSchema, ResumeSchema


def parse_text_with_llm(raw_text: str, doc_type: str = "invoice") -> dict:
    """Uses LLM API to extract structured JSON data from raw text based on document type."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    print(f"\n[DEBUG] Parsing document type: {doc_type}")
    print(f"[DEBUG] Raw text length: {len(raw_text)} characters")

    # 1. Select target schema
    if doc_type.lower() == "invoice":
        schema_format = InvoiceSchema.model_json_schema()
    elif doc_type.lower() == "resume":
        schema_format = ResumeSchema.model_json_schema()
    else:
        raise ValueError(f"Unsupported document type: {doc_type}")

    # 2. System Prompt
    system_prompt = (
        f"You are a high-precision AI document parsing assistant.\n"
        f"Extract facts ONLY from the provided raw document text. Do not invent details.\n"
        f"Strictly output valid JSON matching this schema:\n{json.dumps(schema_format)}\n\n"
        f"Rules:\n"
        f"1. Extract real values directly from the text.\n"
        f"2. Return ONLY a valid JSON object without markdown codeblocks (no ```json).\n"
        f"3. If a field is missing in the text, set it to null or [] (empty list)."
    )

    # 3. Fallback mock data ONLY if API key is missing or default placeholder
    if not api_key or api_key == "your_groq_api_key_here" or not api_key.startswith("gsk_"):
        print("[INFO] Returning structured mock fallback data (No valid GROQ_API_KEY set).")
        if doc_type.lower() == "invoice":
            return {
                "vendor_name": "Apex Software Solutions Inc.",
                "invoice_number": "INV-2026-0042",
                "date": "2026-03-20",
                "due_date": "2026-04-20",
                "items": [
                    {"description": "FastAPI Application Development", "quantity": 1.0, "unit_price": 800.0, "amount": 800.0},
                    {"description": "Docker & Celery Queue Setup", "quantity": 1.0, "unit_price": 400.0, "amount": 400.0},
                    {"description": "LLM API Integration", "quantity": 1.0, "unit_price": 300.0, "amount": 300.0}
                ],
                "subtotal": 1500.0,
                "tax_amount": 120.0,
                "total_amount": 1620.0,
            }
        else:
            return {
                "candidate_name": "Sample Candidate",
                "email": "candidate@example.com",
                "phone": "+91 9876543210",
                "skills": ["Python", "FastAPI", "Docker", "SQL"],
                "experience": [],
                "education": []
            }

    # 4. Live Groq API Call (Using active model: llama-3.1-8b-instant)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "openai/gpt-oss-120b",  # Verified standard Groq endpoint
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"DOCUMENT RAW TEXT:\n---\n{raw_text}\n---"},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }

    url = "https://api.groq.com/openai/v1/chat/completions"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            result_text = response.json()["choices"][0]["message"]["content"]
            return json.loads(result_text)
        else:
            print(f"[ERROR] Groq API call failed with status {response.status_code}: {response.text}")
            raise Exception(f"LLM API Error ({response.status_code}): {response.text}")
    except Exception as err:
        print(f"[ERROR] Exception during LLM parsing: {str(err)}")
        raise err