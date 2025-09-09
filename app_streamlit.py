import streamlit as st
import os
from config import setup_environment
from db_streamlit import (
    initialize_session_state,
    handle_file_upload,
    process_documents,
    handle_chat_interaction
)

# Page configuration
st.set_page_config(
    page_title="PDF RAG System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application function"""
    # Setup environment
    setup_environment()
    
    # Initialize session state
    initialize_session_state()
    
    # App header
    st.title("📄 PDF RAG System")
    st.markdown("Ask questions about your PDF documents!")
    
    # Sidebar for file upload and processing
    with st.sidebar:
        st.header("📁 PDF Document Upload")
        
        # File upload
        uploaded_files = handle_file_upload()
        
        # Process documents button
        if uploaded_files:
            if st.button("🔄 Process Documents", type="primary"):
                with st.spinner("Processing PDF documents..."):
                    success = process_documents(uploaded_files)
                    if success:
                        st.success("PDF documents processed successfully!")
                        st.rerun()
                    else:
                        st.error("Error processing PDF documents")
        
        # Show processing status
        if st.session_state.get('vectorstore_ready', False):
            st.success("✅ PDF documents ready for questions")
        else:
            st.info("📤 Upload and process PDF documents to start")
    
    # Main chat interface
    if st.session_state.get('vectorstore_ready', False):
        handle_chat_interaction()
    else:
        st.info("👆 Please upload and process PDF documents in the sidebar to start asking questions.")

if __name__ == "__main__":
    main()