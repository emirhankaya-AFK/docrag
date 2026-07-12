import streamlit as st
import requests

API_URL = "http://127.0.0.1:8003/api"

st.set_page_config(
    page_title="DocRAG - Developer Documentation Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Developer Look & Feel
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #05070f 0%, #0c101f 100%);
        color: #e2e8f0;
        font-family: 'Consolas', 'Fira Code', 'Monaco', monospace;
    }
    
    h1 {
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .doc-card {
        background: rgba(12, 16, 31, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 254, 0.12);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .doc-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 242, 254, 0.4);
    }
    
    .badge-code {
        background-color: rgba(0, 242, 254, 0.15);
        color: #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.25);
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("💻 DocRAG")
st.subheader("> Developer Documentation Technical Assistant & Code Synthesizer")

st.markdown("""
Welcome to **DocRAG**! This technical assistant indexes library documentation (HTML, Markdown, PDFs), enabling semantic searches, structured endpoint browsing, automatic code extraction, error troubleshooting, and best-practice checks.

### Features Available:
1. **Upload Documentation**: Attach HTML pages, Markdown readmes, or PDF developer guides.
2. **Search Documentation**: Semantic code searches finding parameter signatures and endpoints.
3. **Documentation Q&A**: Code-level Q&A with snippet references.
4. **Code Examples**: Auto-generate custom production-ready integrations.
5. **Troubleshoot**: Paste traceback logs and compiler warnings for diagnostic guidelines.
6. **Best Practices**: View optimized patterns and anti-patterns for framework setups.
""")

try:
    res = requests.get(f"{API_URL}/docs/frameworks")
    if res.status_code == 200:
        frameworks = res.json()
        st.markdown("### 📂 Supported Frameworks & Libraries")
        cols = st.columns(len(frameworks))
        for idx, fw in enumerate(frameworks):
            with cols[idx]:
                st.markdown(f"""
                <div class="doc-card">
                    <h4 style="margin: 0 0 6px 0; color: #fff;">{fw['name']}</h4>
                    <p style="margin: 0 0 10px 0; font-size: 12px; color: #94a3b8;">Language: {fw['language']}</p>
                    <span class="badge-code">Version: {fw['current_version']}</span>
                </div>
                """, unsafe_allow_html=True)
except Exception as e:
    st.warning("Could not connect to DocRAG backend. Make sure the FastAPI server is running on port 8003.")
