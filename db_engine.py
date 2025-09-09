import os
import tempfile
from typing import List, Optional
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
from config import MODEL_CONFIG, VECTOR_CONFIG, validate_api_keys

class PDFRAGEngine:
    """PDF RAG (Retrieval-Augmented Generation) Engine"""
    
    def __init__(self):
        self.vectorstore = None
        self.qa_chain = None
        self.embeddings = None
        self.llm = None
        
        # Validate API keys
        if not validate_api_keys():
            raise ValueError("Missing required API keys")
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize embeddings and LLM models"""
        try:
            self.embeddings = OpenAIEmbeddings(
                model=MODEL_CONFIG["embedding_model"]
            )
            
            self.llm = ChatOpenAI(
                model=MODEL_CONFIG["chat_model"],
                temperature=MODEL_CONFIG["temperature"],
                max_tokens=MODEL_CONFIG["max_tokens"]
            )
        except Exception as e:
            raise Exception(f"Failed to initialize models: {str(e)}")
    
    def process_uploaded_pdf_files(self, uploaded_files) -> bool:
        """Process uploaded PDF files and create vector store"""
        try:
            documents = []
            
            # Create temporary directory for uploaded PDF files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save uploaded PDF files to temporary directory
                for uploaded_file in uploaded_files:
                    if uploaded_file.name.lower().endswith('.pdf'):
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                
                # Load PDF documents from temporary directory
                loader = PyPDFDirectoryLoader(temp_dir)
                documents = loader.load()
            
            if not documents:
                raise ValueError("No PDF documents were loaded")
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=VECTOR_CONFIG["chunk_size"],
                chunk_overlap=VECTOR_CONFIG["chunk_overlap"]
            )
            
            splits = text_splitter.split_documents(documents)
            
            if not splits:
                raise ValueError("No text chunks were created from PDF documents")
            
            # Create vector store
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                collection_name=VECTOR_CONFIG["collection_name"]
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True
            )
            
            return True
            
        except Exception as e:
            print(f"Error processing PDF files: {str(e)}")
            return False
    
    def ask_question_about_pdfs(self, question: str) -> dict:
        """Ask a question about the PDF documents and get an answer with sources"""
        if not self.qa_chain:
            return {
                "answer": "Please upload and process PDF documents first.",
                "sources": []
            }
        
        try:
            result = self.qa_chain.invoke({"query": question})
            
            return {
                "answer": result["result"],
                "sources": result.get("source_documents", [])
            }
            
        except Exception as e:
            return {
                "answer": f"Error processing question about PDF documents: {str(e)}",
                "sources": []
            }
    
    def is_ready(self) -> bool:
        """Check if the PDF RAG engine is ready to answer questions"""
        return self.qa_chain is not None