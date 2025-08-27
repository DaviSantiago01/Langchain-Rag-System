# criar_db.py - Criador do banco de dados vetorial
from langchain_community.document_loaders import PyPDFDirectoryLoader  # Leitor de PDFs (PyPDF = biblioteca para PDFs)
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Divisor de texto (Recursive = recursivo, divide inteligentemente)
from langchain_chroma import Chroma  # Banco de dados vetorial (Chroma = tipo específico de banco)
from langchain_openai import OpenAIEmbeddings  # Embeddings da OpenAI (converte texto em vetores)
from dotenv import load_dotenv  # Carrega variáveis do arquivo .env
import os  # Operações do sistema operacional (criar pastas, verificar arquivos)
import shutil  # Utilitários para arquivos (copiar, mover, deletar)

print("Iniciando criação do banco de dados...")
load_dotenv()

PASTA_BASE = "base"  # Pasta com os PDFs
CAMINHO_DB = "db"    # Pasta do banco de dados

def criar_db():
    """
    Esta função serve para:
    1. Verificar se existem PDFs na pasta base
    2. Carregar todos os documentos PDF
    3. Dividir em pequenos pedaços (chunks)
    4. Converter em embeddings e salvar no banco
    """
    
    try:
        print("\n--- Processo de criação do banco iniciado ---")
        
        # 1. Verificar se pasta existe
        if not os.path.exists(PASTA_BASE):  # os.path.exists() = verifica se pasta/arquivo existe
            print(f"Pasta '{PASTA_BASE}' não encontrada. Criando...")
            os.makedirs(PASTA_BASE)  # os.makedirs() = cria pasta (make directories)
            print("Adicione seus arquivos PDF na pasta 'base' e execute novamente.")
            return

        print("Pasta base encontrada!")

        # 2. Carregar documentos
        print("Carregando documentos PDF...")
        documentos = carregar_documentos()
        
        if not documentos:
            print("Nenhum documento encontrado na pasta base.")
            return

        print(f"Documentos carregados: {len(documentos)}")
        
        # 3. Dividir em chunks
        print("Dividindo documentos em pedaços menores...")
        chunks = dividir_documentos(documentos)
        print(f"Chunks criados: {len(chunks)}")
        
        # 4. Criar banco de dados
        print("Criando banco de dados vetorial...")
        vetorizar_chunks(chunks)
        print("Banco de dados criado com sucesso!")

    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")

def carregar_documentos():
    """
    Esta função serve para:
    1. Ler todos os arquivos PDF da pasta base
    2. Retornar lista de documentos carregados
    """
    
    try:  # try/except = tenta executar, se der erro captura
        carregador = PyPDFDirectoryLoader(PASTA_BASE)  # Cria leitor que busca todos PDFs da pasta
        documentos = carregador.load()  # .load() = carrega e converte PDFs em texto
        return documentos
    except Exception as e:  # Se der erro na leitura dos PDFs
        print(f"Erro ao carregar documentos: {e}")
        return []  # Retorna lista vazia

def dividir_documentos(documentos):
    """
    Esta função serve para:
    1. Dividir documentos grandes em pedaços menores
    2. Cada pedaço terá no máximo 1000 caracteres
    3. Criar sobreposição de 200 caracteres entre pedaços
    """
    
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Tamanho máximo de cada pedaço em caracteres
        chunk_overlap=200,    # Sobreposição entre pedaços (overlap = sobreposição)
        length_function=len,  # Função para medir tamanho (len = length/comprimento)
        add_start_index=True, # Adicionar índice de onde começa no documento original
    )
    chunks = separador_documentos.split_documents(documentos)  # .split_documents() = divide documentos em chunks
    return chunks

def vetorizar_chunks(chunks):
    """
    Esta função serve para:
    1. Remover banco antigo se existir
    2. Converter chunks em embeddings (vetores)
    3. Salvar no banco de dados Chroma
    """
    
    # Remover banco antigo se existir
    if os.path.exists(CAMINHO_DB):  # Verifica se pasta do banco existe
        print("Removendo banco antigo...")
        shutil.rmtree(CAMINHO_DB)  # shutil.rmtree() = remove pasta e todo conteúdo (rm = remove, tree = árvore)
    
    # Criar novo banco com embeddings
    db = Chroma.from_documents(
        chunks,                 # Lista de chunks para processar
        OpenAIEmbeddings(),    # Função que converte texto em vetores numéricos
        persist_directory=CAMINHO_DB  # persist = persistir/salvar permanentemente
    )
    print(f"Banco de dados salvo em: {CAMINHO_DB}")

if __name__ == "__main__":
    criar_db()