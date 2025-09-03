import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

print("Iniciando criação do banco de dados...")
load_dotenv()

BASE_FOLDER_PATH = "base"
DB_PATH = "chroma_db"

def criar_db():
    try:
        if not os.path.exists(BASE_FOLDER_PATH):
            print(f"[ERRO] Erro: Pasta '{BASE_FOLDER_PATH}' não encontrada!")
            print(f"   Crie a pasta '{BASE_FOLDER_PATH}' e coloque seus arquivos PDF nela.")
            return False
        
        arquivos_pdf = [f for f in os.listdir(BASE_FOLDER_PATH) if f.lower().endswith('.pdf')]
        if not arquivos_pdf:
            print(f"[ERRO] Erro: Nenhum arquivo PDF encontrado na pasta '{BASE_FOLDER_PATH}'!")
            print("   Adicione pelo menos um arquivo PDF na pasta.")
            return False
        
        print(f"[PASTA] Encontrados {len(arquivos_pdf)} arquivo(s) PDF:")
        for arquivo in arquivos_pdf:
            print(f"   - {arquivo}")
        
        if os.path.exists(DB_PATH):
            print(f"[REMOVE] Removendo banco de dados antigo...")
            shutil.rmtree(DB_PATH)
            print("   Banco antigo removido com sucesso!")
        
        print("[DOCS] Carregando documentos PDF...")
        loader = PyPDFDirectoryLoader(BASE_FOLDER_PATH)
        documentos = loader.load()
        print(f"   [OK] {len(documentos)} página(s) carregada(s) com sucesso!")
        
        total_caracteres = sum(len(doc.page_content) for doc in documentos)
        print(f"   [INFO] Total de caracteres: {total_caracteres:,}")
        
        print("[SPLIT] Dividindo textos em chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documentos)
        print(f"   [OK] Texto dividido em {len(chunks)} chunk(s)!")
        
        tamanhos_chunks = [len(chunk.page_content) for chunk in chunks]
        tamanho_medio = sum(tamanhos_chunks) / len(tamanhos_chunks)
        print(f"   [INFO] Tamanho médio dos chunks: {tamanho_medio:.0f} caracteres")
        
        print("[AI] Criando embeddings e salvando no banco de dados...")
        print("   [AGUARDE] Este processo pode demorar alguns minutos...")
        
        embeddings = OpenAIEmbeddings()
        
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_PATH
        )
        
        print("   [OK] Banco de dados criado com sucesso!")
        
        print("[TESTE] Testando o banco de dados...")
        teste_busca = db.similarity_search("teste", k=1)
        if teste_busca:
            print("   [OK] Teste realizado com sucesso!")
            print(f"   [PAGINA] Exemplo de conteúdo encontrado: {teste_busca[0].page_content[:100]}...")
        else:
            print("   [AVISO] Aviso: Teste não retornou resultados, mas o banco foi criado.")
        
        print("\n[SUCESSO] Processo concluído com sucesso!")
        print(f"[PASTA] Banco de dados salvo em: {os.path.abspath(DB_PATH)}")
        print("\n[DICA] Agora você pode executar 'python main.py' para fazer perguntas!")
        
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro durante a criação do banco: {e}")
        print("\n[SOLUCAO] Possíveis soluções:")
        print("   1. Verifique se a API key da OpenAI está configurada")
        print("   2. Verifique sua conexão com a internet")
        print("   3. Verifique se os arquivos PDF não estão corrompidos")
        return False

if __name__ == "__main__":
    criar_db()