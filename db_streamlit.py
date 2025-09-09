import streamlit as st
from typing import List
from db_engine import PDFRAGEngine

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'pdf_rag_engine' not in st.session_state:
        try:
            st.session_state.pdf_rag_engine = PDFRAGEngine()
        except Exception as e:
            st.error(f"Failed to initialize PDF RAG engine: {str(e)}")
            st.stop()
    
    if 'vectorstore_ready' not in st.session_state:
        st.session_state.vectorstore_ready = False
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def handle_file_upload():
    """Handle PDF file upload in the sidebar"""
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more PDF documents to ask questions about"
    )
    
    if uploaded_files:
        st.write(f"📄 {len(uploaded_files)} PDF file(s) uploaded")
        for file in uploaded_files:
            st.write(f"• {file.name}")
    
    return uploaded_files

def process_documents(uploaded_files) -> bool:
    """Process uploaded PDF documents and create vector store"""
    try:
        success = st.session_state.pdf_rag_engine.process_uploaded_pdf_files(uploaded_files)
        
        if success:
            st.session_state.vectorstore_ready = True
            # Clear chat history when new PDF documents are processed
            st.session_state.chat_history = []
        
        return success
        
    except Exception as e:
        st.error(f"Error processing PDF documents: {str(e)}")
        return False

def handle_chat_interaction():
    """Handle chat interaction in the main area"""
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Show sources for assistant messages
            if message["role"] == "assistant" and "sources" in message:
                if message["sources"]:
                    with st.expander("📚 PDF Sources", expanded=False):
                        for i, source in enumerate(message["sources"], 1):
                            st.write(f"**PDF Source {i}:**")
                            st.write(source.page_content[:300] + "..." if len(source.page_content) > 300 else source.page_content)
                            if hasattr(source, 'metadata') and source.metadata:
                                st.write(f"*Metadata: {source.metadata}*")
                            st.divider()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your PDF documents..."):
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Searching through PDF documents..."):
                result = st.session_state.pdf_rag_engine.ask_question_about_pdfs(prompt)
                
                st.write(result["answer"])
                
                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"]
                })
                
                # Show PDF sources
                if result["sources"]:
                    with st.expander("📚 PDF Sources", expanded=False):
                        for i, source in enumerate(result["sources"], 1):
                            st.write(f"**PDF Source {i}:**")
                            st.write(source.page_content[:300] + "..." if len(source.page_content) > 300 else source.page_content)
                            if hasattr(source, 'metadata') and source.metadata:
                                st.write(f"*Metadata: {source.metadata}*")
                            st.divider()
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()