# PDF RAG System

A simple and efficient PDF-based Retrieval-Augmented Generation (RAG) system built with Langchain, Streamlit, and ChromaDB.

## Features

- **PDF Document Processing**: Upload and process PDF documents
- **Vector Storage**: Efficient document embedding storage with ChromaDB
- **Interactive Chat**: Ask questions about your PDF documents
- **Streamlit Interface**: Clean and user-friendly web interface
- **Multiple LLM Support**: Compatible with various language models

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/DaviSantiago01/PDF-RAG-System.git
cd PDF-RAG-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app_streamlit.py
```

## Usage

1. **Upload PDF Documents**: Use the sidebar to upload PDF files
2. **Process Documents**: Click "Process Documents" to create embeddings
3. **Ask Questions**: Type your questions in the chat interface
4. **Get Answers**: Receive contextual answers based on your PDF documents

## Project Structure

```
PDF-RAG-System/
├── app_streamlit.py      # Main Streamlit application
├── config.py             # Configuration settings
├── db_engine.py          # Database and vector store logic
├── db_streamlit.py       # Streamlit database interface
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version for deployment
└── README.md            # Project documentation
```

## Configuration

The system uses environment variables for configuration:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `LANGCHAIN_API_KEY`: Langchain API key (optional)
- `LANGCHAIN_TRACING_V2`: Enable Langchain tracing (optional)

## Dependencies

Key dependencies include:

- **Streamlit**: Web interface framework
- **Langchain**: LLM application framework
- **ChromaDB**: Vector database for embeddings
- **OpenAI**: Language model API
- **PyPDF**: PDF document processing

## Deployment

This application is configured for easy deployment on:

- **Streamlit Cloud**: Direct deployment from GitHub
- **Heroku**: Using the included runtime.txt
- **Local**: Run directly with Python

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please open an issue on GitHub or contact the maintainer.

---

**Built with ❤️ using Langchain and Streamlit**