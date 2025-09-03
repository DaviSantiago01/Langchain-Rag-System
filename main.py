from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "db"

PROMPT_TEMPLATE = """ 
Analise os documentos abaixo e responda a pergunta do usuário.

PERGUNTA: {pergunta}

DOCUMENTOS:
{documentos}

INSTRUÇÕES:
- Use APENAS as informações dos documentos fornecidos
- Se a resposta estiver nos documentos, responda de forma clara e completa
- Se não encontrar informações suficientes, responda: "Não encontrei essa informação nos documentos fornecidos"
- Seja específico e cite as informações relevantes que encontrou
"""

def conectar_database():
    """Conecta ao banco de dados ChromaDB."""
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

def buscar_documentos_relevantes(db, pergunta, k=3, threshold=0.5):
    """Busca documentos relevantes no banco de dados."""
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=k)
    
    if len(resultados) == 0 or resultados[0][1] < threshold:
        return None
    
    return resultados

def gerar_resposta(pergunta, documentos):
    """Gera resposta usando OpenAI com base nos documentos encontrados."""
    textos_documentos = [doc[0].page_content for doc in documentos]
    contexto = "\n\n----\n\n".join(textos_documentos)
    
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt_formatado = prompt.invoke({"pergunta": pergunta, "documentos": contexto})
    
    modelo = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=1000)
    resposta = modelo.invoke(prompt_formatado)
    
    return resposta.content
