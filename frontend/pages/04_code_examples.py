import streamlit as st
import requests
from components.code_viewer import CodeViewerComponent

API_URL = "http://127.0.0.1:8003/api"

st.title("🎛️ Code Example Synthesizer")

try:
    fw_res = requests.get(f"{API_URL}/docs/frameworks")
    frameworks = fw_res.json() if fw_res.status_code == 200 else []
except Exception:
    frameworks = []

tab1, tab2 = st.tabs(["💡 Generate Custom Integration", "📚 Browse Code Patterns"])

with tab1:
    st.markdown("### Generate Custom Copy-Paste Examples")
    fw_options = {"All Frameworks": None}
    for fw in frameworks:
        fw_options[fw["name"]] = fw["id"]
        
    sel_name = st.selectbox("Select Target Framework", list(fw_options.keys()), key="gen_fw")
    sel_id = fw_options[sel_name]
    
    task = st.text_input("Describe the coding task/integration you want to generate:", placeholder="e.g. Create a CRUD endpoint that saves user data to PostgreSQL")
    
    if st.button("Generate Code Example") and task:
        with st.spinner("Synthesizing code based on documentation specifications..."):
            try:
                res = requests.post(f"{API_URL}/examples/generate", json={
                    "task": task,
                    "framework_id": sel_id
                })
                if res.status_code == 200:
                    code_data = res.json()
                    st.write("")
                    CodeViewerComponent.render_code(code_data["code"], language="python", title="Synthesized Production-Ready Code")
                else:
                    st.error("Failed to generate code.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

with tab2:
    st.markdown("### Pre-parsed Code Patterns")
    fw_filter = st.selectbox("Filter Patterns", ["All"] + [fw["name"] for fw in frameworks])
    
    params = {}
    if fw_filter != "All":
        params["framework"] = fw_filter
        
    try:
        ex_res = requests.get(f"{API_URL}/examples/", params=params)
        if ex_res.status_code == 200:
            examples = ex_res.json()
            if not examples:
                st.info("No code snippets parsed for this framework yet.")
            else:
                for idx, ex in enumerate(examples):
                    with st.expander(f"🔹 {ex['task_description']} ({ex['language'].upper()})"):
                        st.markdown(f"**Tags:** {', '.join(ex['tags'])}")
                        CodeViewerComponent.render_code(ex["code_block"], language=ex["language"])
    except Exception as e:
        st.error(f"Failed to fetch examples: {e}")
