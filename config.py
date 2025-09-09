import os
import streamlit as st
from typing import Optional

def setup_environment() -> None:
    """Setup environment variables and API keys"""
    
    # OpenAI API Key
    openai_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    
    # Langchain API Key (optional)
    langchain_key = st.secrets.get("LANGCHAIN_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
    if langchain_key:
        os.environ["LANGCHAIN_API_KEY"] = langchain_key
        os.environ["LANGCHAIN_TRACING_V2"] = "true"

def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment or Streamlit secrets"""
    return os.getenv("OPENAI_API_KEY")

def validate_api_keys() -> bool:
    """Validate that required API keys are present"""
    openai_key = get_openai_api_key()
    
    if not openai_key:
        st.error("❌ OpenAI API key not found. Please set OPENAI_API_KEY in your environment or Streamlit secrets.")
        st.info("💡 You can get an API key from: https://platform.openai.com/api-keys")
        return False
    
    return True

# Model configurations
MODEL_CONFIG = {
    "embedding_model": "text-embedding-3-small",
    "chat_model": "gpt-3.5-turbo",
    "temperature": 0.1,
    "max_tokens": 1000
}

# Vector store configuration
VECTOR_CONFIG = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "collection_name": "pdf_documents"
}