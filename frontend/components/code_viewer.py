import streamlit as st

class CodeViewerComponent:
    @staticmethod
    def render_code(code_block: str, language: str = "python", title: str = None):
        """
        Renders code block inside a code box with copy functionality.
        """
        if title:
            st.markdown(f"**{title} ({language.upper()}):**")
        st.code(code_block, language=language)
