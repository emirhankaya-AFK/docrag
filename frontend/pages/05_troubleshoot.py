import streamlit as st
import requests
from components.error_explainer import ErrorExplainerComponent

API_URL = "http://127.0.0.1:8003/api"

st.title("🛠️ Runtime Error Troubleshooter")

try:
    fw_res = requests.get(f"{API_URL}/docs/frameworks")
    frameworks = fw_res.json() if fw_res.status_code == 200 else []
except Exception:
    frameworks = []

fw_options = {"All Frameworks": None}
for fw in frameworks:
    fw_options[fw["name"]] = fw["id"]
    
selected_name = st.selectbox("Select Target Framework", list(fw_options.keys()))
selected_id = fw_options[selected_name]

st.markdown("Paste your error output (compiler exceptions, runtime logs, tracebacks):")

error_log = st.text_area("Stacktrace / Error Message:", height=180, placeholder="e.g. TypeError: cannot unpack non-iterable NoneType object")

if st.button("Analyze & Troubleshoot") and error_log:
    with st.spinner("Checking error catalog and querying documentation..."):
        try:
            res = requests.post(f"{API_URL}/troubleshoot/", json={
                "error_message": error_log,
                "framework_id": selected_id
            })
            if res.status_code == 200:
                ErrorExplainerComponent.render_explanation(res.json())
            else:
                st.error("Error troubleshooting request failed.")
        except Exception as e:
            st.error(f"Failed to troubleshoot error: {e}")
