import streamlit as st
import requests

API_URL = "http://127.0.0.1:8003/api"

st.title("📂 Upload Framework Documentation")

try:
    fw_res = requests.get(f"{API_URL}/docs/frameworks")
    frameworks = fw_res.json() if fw_res.status_code == 200 else []
except Exception:
    frameworks = []

if not frameworks:
    st.warning("FastAPI backend is offline or no frameworks registered in SQLite database.")
else:
    fw_options = {fw["name"]: fw["id"] for fw in frameworks}
    selected_name = st.selectbox("Select Target Framework", list(fw_options.keys()))
    selected_id = fw_options[selected_name]
    
    with st.form("upload_form", clear_on_submit=True):
        uploaded_file = st.file_uploader("Select Documentation File (HTML, MD, PDF, TXT)", type=["html", "md", "pdf", "txt"])
        submit_btn = st.form_submit_button("Upload and Process Documentation")
        
        if submit_btn and uploaded_file:
            with st.spinner("Extracting text and structure in background..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/octet-stream")}
                    res = requests.post(f"{API_URL}/docs/{selected_id}/upload", files=files)
                    if res.status_code == 200:
                        st.success("Successfully uploaded! Documentation parser & code block extractor triggered in background.")
                    else:
                        st.error("Failed to upload documentation.")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

# Listing active files
st.write("---")
st.markdown("### 📚 Stored Documentation Indexes")
for fw in frameworks:
    st.markdown(f"#### Framework: {fw['name']} ({fw['current_version']})")
    try:
        docs_res = requests.get(f"{API_URL}/docs/{fw['id']}")
        if docs_res.status_code == 200:
            docs = docs_res.json()
            if not docs:
                st.caption("No files uploaded for this framework.")
            else:
                for d in docs:
                    c1, c2, c3 = st.columns([6, 2, 2])
                    with c1:
                        st.markdown(f"- 📄 {d['file_name']}")
                    with c2:
                        st.caption(f"Uploaded: {d['uploaded_at'][:10]}")
                    with c3:
                        if st.button("Delete 🗑️", key=d["id"]):
                            with st.spinner("Deleting index..."):
                                requests.delete(f"{API_URL}/docs/{d['id']}")
                                st.rerun()
    except Exception as e:
        st.error(f"Failed to fetch documents: {e}")
