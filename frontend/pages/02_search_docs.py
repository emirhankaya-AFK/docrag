import streamlit as st
import requests
from components.doc_browser import DocBrowserComponent

API_URL = "http://127.0.0.1:8003/api"

st.title("🔍 Semantic Documentation Search")

try:
    fw_res = requests.get(f"{API_URL}/docs/frameworks")
    frameworks = fw_res.json() if fw_res.status_code == 200 else []
except Exception:
    frameworks = []

fw_options = {"All Frameworks": None}
for fw in frameworks:
    fw_options[fw["name"]] = fw["id"]
    
selected_name = st.selectbox("Filter by Framework", list(fw_options.keys()))
selected_id = fw_options[selected_name]

query = st.text_input("Enter search query:", placeholder="e.g. raise HTTPException in fastapi, register database connection")

if st.button("Search docs") and query:
    params = {"query": query}
    if selected_id:
        params["framework_id"] = selected_id
        
    with st.spinner("Searching vector index..."):
        try:
            res = requests.get(f"{API_URL}/search/", params=params)
            if res.status_code == 200:
                results = res.json()
                
                # Fetch structural details if possible
                details_res = requests.get(f"{API_URL}/search/details", params=params)
                if details_res.status_code == 200:
                    details = details_res.json()
                    if details.get("name") != "No match found":
                        st.markdown("### 🏷️ Identified Reference")
                        st.markdown(f"""
                        <div style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.15); border-radius: 8px; padding: 20px; margin-bottom: 24px;">
                            <strong style="color: #00f2fe; font-size: 16px;">{details.get('name')}</strong><br>
                            <code style="color: #fff; font-size: 13px;">Signature: {details.get('parameters')}</code>
                            <p style="margin: 12px 0 0 0; font-size: 13px; color: #cbd5e1;">{details.get('description')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if details.get("code_example"):
                            st.markdown("**Example Usage:**")
                            st.code(details["code_example"], language="python")
                            st.write("---")
                            
                st.markdown("### 📄 Matching Documentation Chunks")
                if not results:
                    st.info("No matching chunks found in database.")
                else:
                    for idx, snippet in enumerate(results):
                        DocBrowserComponent.render_doc_snippet(snippet, idx)
            else:
                st.error("Error search.")
        except Exception as e:
            st.error(f"Search failed: {e}")
