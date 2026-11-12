# ⚡ NEXUS AI — Document Intelligence Studio

An AI-powered document parser built with **FastAPI**, **Groq LPU (`openai/gpt-oss-120b`)**, and **Streamlit** to extract clean, schema-validated JSON from unstructured invoices, receipts, and PDFs.

---

## ✨ Features
- **Ultra-Fast AI Extraction:** Powered by Groq LPU inference using `openai/gpt-oss-120b`.
- **RESTful Backend:** Built with FastAPI (`/api/v1/parse`) supporting multiple document schemas (`invoice`, `receipt`, `resume`, `contract`, `general`).
- **Modern Glassmorphism UI:** Interactive Streamlit dashboard with live KPI metrics, structured data tables, and one-click JSON export.
- **Docker Ready:** Includes `Dockerfile` and `docker-compose.yml` for containerized deployment.

---

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Uvicorn
- **AI / LLM:** Groq API (`openai/gpt-oss-120b`)
- **Frontend:** Streamlit, Pandas, Requests
- **Deployment:** Docker & Docker Compose

---

## 📁 Project Structure
```text
ai-document-parser/
├── app/
│   ├── api/            # API routes & endpoints
│   ├── core/           # Text extractor & LLM parser logic
│   ├── schemas/        # Pydantic data validation models
│   ├── workers/        # Background task workers
│   ├── dashboard.py    # Streamlit frontend UI
│   └── main.py         # FastAPI entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

###########################################################################################################################

🚀 How to Run Locally


1. Clone the Repository
Bash
git clone [https://github.com/YOUR_USERNAME/ai-document-parser.git](https://github.com/YOUR_USERNAME/ai-document-parser.git)
cd ai-document-parser


2. Create & Activate Virtual Environment
Windows (PowerShell):

PowerShell
python -m venv .venv
.\.venv\Scripts\activate


Linux / macOS:
Bash
python3 -m venv .venv
source .venv/bin/activate


3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory and add your Groq API key:

4. Code snippet
GROQ_API_KEY=gsk_your_groq_api_key_here


5. Start the Application (2 Terminals)
Terminal 1 — Start FastAPI Backend:

Bash
uvicorn app.main:app --reload
API Docs available at: http://127.0.0.1:8000/docs