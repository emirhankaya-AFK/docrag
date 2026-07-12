import streamlit as st
import requests

API_URL = "http://127.0.0.1:8003/api"

st.title("💬 Ask Technical Assistant")

try:
    fw_res = requests.get(f"{API_URL}/docs/frameworks")
    frameworks = fw_res.json() if fw_res.status_code == 200 else []
except Exception:
    frameworks = []

fw_options = {"All Frameworks": None}
for fw in frameworks:
    fw_options[fw["name"]] = fw["id"]
    
selected_name = st.selectbox("Select Framework", list(fw_options.keys()))
selected_id = fw_options[selected_name]

question = st.text_input("Enter your technical question:", placeholder="e.g. How do I authenticate with a custom OAuth2 token flow?")

if st.button("Ask Assistant") and question:
    with st.spinner("Analyzing doc embeddings..."):
        try:
            payload = {"question": question}
            if selected_id:
                payload["framework_id"] = selected_id
                
            res = requests.post(f"{API_URL}/qa/ask", json=payload)
            if res.status_code == 200:
                data = res.json()
                
                st.write("")
                st.markdown("### 🤖 Answer")
                st.markdown(f'<div style="background: rgba(12, 16, 31, 0.4); border-left: 4px solid #00f2fe; border-radius: 8px; padding: 20px; color: #f1f5f9; line-height: 1.6;">{data["answer"]}</div>', unsafe_allow_html=True)
                
                st.write("")
                st.markdown("### 📋 Evidence References")
                if not data.get("sources"):
                    st.caption("No sources matched in ChromaDB.")
                else:
                    for idx, src in enumerate(data["sources"]):
                        st.markdown(f"""
                        <div style="background: rgba(12, 16, 31, 0.2); border: 1px solid rgba(255,255,255,0.04); border-radius: 6px; padding: 12px; margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px;">
                                <strong style="color: #00f2fe;">Reference #{idx+1}: {src['file_name']}</strong>
                                <span style="color: #10b981; font-weight: bold;">Score: {src['score']:.2f}</span>
                            </div>
                            <p style="font-size: 13px; color: #cbd5e1; font-style: italic; margin: 0;">"... {src['snippet']} ..."</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Error generating answer.")
        except Exception as e:
            st.error(f"Failed to query assistant: {e}")
