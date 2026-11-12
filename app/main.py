from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
import sys
import asyncio

load_dotenv()
# Silence the Windows-specific ProactorEventLoop connection reset bug
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


app = FastAPI(
    title="AI Document Processing & Extraction API",
    description="Scalable pipeline to extract and structure unstructured data from PDFs using Python & LLMs.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API endpoints
app.include_router(api_router)


@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "message": "AI Document Processing Engine is operational.",
        "docs_url": "/docs"
    }