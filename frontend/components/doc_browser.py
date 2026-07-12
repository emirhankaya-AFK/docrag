import streamlit as st
from typing import Dict, Any

class DocBrowserComponent:
    @staticmethod
    def render_doc_snippet(snippet: Dict[str, Any], idx: int):
        """
        Renders a retrieved documentation block in a neat terminal layout.
        """
        file_name = snippet["metadata"].get("file_name", "doc_page.html")
        score = snippet.get("score", 1.0)
        
        st.markdown(f"""
        <div style="background: rgba(12, 16, 31, 0.4); border-left: 3px solid #00f2fe; border-radius: 4px; padding: 12px; margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #00f2fe; margin-bottom: 6px;">
                <strong>Snippet #{idx+1} [Source: {file_name}]</strong>
                <strong>Match: {score*100:.1f}%</strong>
            </div>
            <pre style="margin: 0; white-space: pre-wrap; font-size: 12px; color: #cbd5e1; font-family: monospace;">{snippet['text']}</pre>
        </div>
        """, unsafe_allow_html=True)
