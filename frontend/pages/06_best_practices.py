import streamlit as st
import requests

API_URL = "http://127.0.0.1:8003/api"

st.title("🛡️ Architectural Best Practices")

try:
    fw_res = requests.get(f"{API_URL}/docs/frameworks")
    frameworks = fw_res.json() if fw_res.status_code == 200 else []
except Exception:
    frameworks = []

fw_options = {"All Frameworks": None}
for fw in frameworks:
    fw_options[fw["name"]] = fw["id"]
    
selected_name = st.selectbox("Select Library", list(fw_options.keys()))
selected_id = fw_options[selected_name]

topic = st.text_input("Enter pattern topic:", placeholder="e.g. database setup, dependency injection, authentication")

if st.button("Check Guidelines") and topic:
    params = {"topic": topic}
    if selected_id:
        params["framework_id"] = selected_id
        
    with st.spinner("Extracting guidelines..."):
        try:
            res = requests.get(f"{API_URL}/best-practices/", params=params)
            if res.status_code == 200:
                data = res.json()
                st.write("---")
                st.markdown("### 🏆 Architectural Guidelines Report")
                st.markdown(data["report"])
            else:
                st.error("Error fetching guidelines.")
        except Exception as e:
            st.error(f"Failed to fetch practices: {e}")
