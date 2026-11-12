import streamlit as st
import requests
import json
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS AI | Document Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS: DARK GLASSMORPHISM (OBSIDIAN + ELECTRIC VIOLET + CYAN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Dark Theme */
    .stApp {
        background: radial-gradient(circle at top right, #1E1B4B 0%, #090D16 45%, #05070B 100%);
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Glass Effect */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(139, 92, 246, 0.25);
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }

    /* Hide Default Streamlit Top Header Line */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Hero Banner with Neon Glow */
    .hero-box {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.16) 0%, rgba(6, 182, 212, 0.12) 100%);
        border: 1px solid rgba(139, 92, 246, 0.4);
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.15);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        backdrop-filter: blur(12px);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FFFFFF 0%, #C4B5FD 50%, #67E8F9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-sub {
        color: #94A3B8;
        font-size: 0.98rem;
        margin-top: 0.4rem;
    }
    .badge {
        display: inline-block;
        background: rgba(6, 182, 212, 0.15);
        color: #22D3EE;
        border: 1px solid rgba(6, 182, 212, 0.4);
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.6rem;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }

    /* Neon Gradient Primary Button */
    .stButton > button {
        background: linear-gradient(90deg, #7C3AED 0%, #06B6D4 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.5rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
        transition: all 0.25s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(6, 182, 212, 0.55);
    }

    /* Download Button */
    .stDownloadButton > button {
        background: rgba(139, 92, 246, 0.15);
        color: #C4B5FD !important;
        border: 1px solid #8B5CF6;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stDownloadButton > button:hover {
        background: #8B5CF6;
        color: #FFFFFF !important;
    }

    /* File Uploader Dropzone */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.45);
        border: 1.5px dashed #8B5CF6;
        border-radius: 14px;
        padding: 1rem;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #22D3EE;
        background: rgba(30, 41, 59, 0.7);
    }

    /* Metric KPI Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem;
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        color: #22D3EE !important;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
    }

    /* Modern Pill Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 23, 42, 0.8);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        padding: 8px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #7C3AED, #2563EB) !important;
        color: #FFFFFF !important;
    }

    /* Headings */
    h1, h2, h3 {
        color: #F1F5F9 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚡ NEXUS PARSER")
    st.caption("AI-Powered Document Intelligence")
    st.markdown("---")


    api_url = st.text_input(
        "API Endpoint",
        value="https://ai-document-parser-665l.onrender.com/api/v1/parse"
    )
    
    doc_type = st.selectbox(
        "Document Schema",
        options=["invoice", "receipt", "resume", "contract", "general"],
        index=0
    )

    st.markdown("---")
    if st.button("📡 Ping Backend Server"):
        try:
            base_url = api_url.split("/api/")[0]
            res = requests.get(base_url, timeout=3)
            if res.status_code == 200:
                st.success("Connected • 200 OK")
            else:
                st.warning(f"Status: {res.status_code}")
        except Exception:
            st.error("Offline • Start Uvicorn")

    st.markdown("---")
    st.markdown("`ENGINE: openai/gpt-oss-120b`")
    st.markdown("`LATENCY: Ultra-Fast Groq LPU`")

# --- HERO HEADER ---
st.markdown("""
<div class="hero-box">
    <span class="badge">● GROQ LPU ACCELERATED</span>
    <div class="hero-title">AI Document Intelligence Studio</div>
    <div class="hero-sub">Drop any unstructured invoice, receipt, or PDF to extract schema-validated JSON in milliseconds.</div>
</div>
""", unsafe_allow_html=True)

# --- WORKSPACE COLUMNS ---
col1, col2 = st.columns([1, 1.35], gap="large")

with col1:
    st.markdown("#### 01 / Document Input")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drag & drop file here",
        type=["pdf", "png", "jpg", "jpeg", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.markdown(f"""
        <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); 
                    padding: 10px 14px; border-radius: 10px; margin: 10px 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">
            📄 <b>{uploaded_file.name}</b> • {round(uploaded_file.size / 1024, 1)} KB
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_file.type.startswith("image/"):
            st.image(uploaded_file, use_container_width=True)

        extract_btn = st.button("⚡ Run AI Extraction")
    else:
        extract_btn = False
        st.markdown("<p style='color:#64748B; text-align:center; margin-top:1rem;'>Supports PDF, PNG, JPG, TXT</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("#### 02 / Structured Intelligence")
    
    if extract_btn and uploaded_file is not None:
        with st.spinner("⚡ Processing via Groq LPU..."):
            try:
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                params = {"doc_type": doc_type}

                response = requests.post(api_url, params=params, files=files, timeout=30)

                if response.status_code == 200:
                    st.session_state["parsed_result"] = response.json()
                    st.toast("Extraction Complete!", icon="⚡")
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("Backend unreachable. Run `uvicorn app.main:app --reload` first.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    if "parsed_result" in st.session_state:
        data = st.session_state["parsed_result"]
        extracted = data.get("data", data.get("parsed_data", data))

        # Top KPI Metrics
        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("SCHEMA", doc_type.upper())
        with k2:
            total_val = extracted.get("total_amount") or extracted.get("total") or extracted.get("grand_total") or "—"
            st.metric("TOTAL VALUE", str(total_val))
        with k3:
            inv_num = extracted.get("invoice_number") or extracted.get("invoice_id") or extracted.get("date") or "VERIFIED"
            st.metric("REFERENCE", str(inv_num))

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["✨ Visual Data Grid", "🧬 Raw JSON Payload"])

        with tab1:
            if isinstance(extracted, dict):
                flat_fields = {k: v for k, v in extracted.items() if not isinstance(v, (list, dict))}
                list_fields = {k: v for k, v in extracted.items() if isinstance(v, list)}

                if flat_fields:
                    df_meta = pd.DataFrame(list(flat_fields.items()), columns=["Field", "Extracted Value"])
                    st.dataframe(df_meta, use_container_width=True, hide_index=True)

                for key, items in list_fields.items():
                    if items and isinstance(items[0], dict):
                        st.markdown(f"**{key.replace('_', ' ').title()}**")
                        st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
            else:
                st.write(extracted)

        with tab2:
            st.json(data)

        st.download_button(
            label="⬇️ Export JSON Artifact",
            data=json.dumps(data, indent=4),
            file_name=f"nexus_{doc_type}.json",
            mime="application/json"
        )
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 4rem 1.5rem; border-style: dashed;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔮</div>
            <h4 style="margin: 0; color: #E2E8F0;">Awaiting Document Stream</h4>
            <p style="color: #64748B; font-size: 0.9rem; margin-top: 0.4rem;">
                Upload a file on the left and hit <b>Run AI Extraction</b> to visualize structured fields.
            </p>
        </div>
        """, unsafe_allow_html=True)