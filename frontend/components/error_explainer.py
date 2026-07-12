import streamlit as st
from typing import Dict, Any

class ErrorExplainerComponent:
    @staticmethod
    def render_explanation(report: Dict[str, Any]):
        """
        Renders the troubleshooting guide.
        """
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; padding: 20px; margin-bottom: 20px;">
            <h4 style="color: #f87171; margin-top: 0;">❌ Error Diagnostics</h4>
            <p style="font-size: 14px; margin: 0; color: #cbd5e1;"><strong>Type:</strong> {report.get('error_type', 'Exception')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔍 Root Cause Analysis")
        st.write(report.get("root_cause", "No analysis resolved."))
        
        st.write("")
        st.markdown("### 🛠️ Step-by-Step Fix Instructions")
        st.markdown(report.get("fix_steps", "No fix instructions resolved."))
        
        if report.get("corrected_code"):
            st.write("")
            st.markdown("### 💡 Corrected Code Example")
            st.code(report["corrected_code"], language="python")
