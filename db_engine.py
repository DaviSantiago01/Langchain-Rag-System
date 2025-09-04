import os
import shutil
import time
import gc
import psutil
from pathlib import Path
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from config import *

class MotorBanco:
    """Motor simples para criar banco vetorial RAG"""
    
    def __init__(self, pasta_documentos=PASTA_BASE, caminho_banco=CAMINHO_BANCO):
        self.pasta_documentos = pasta_documentos
        self.caminho_banco = caminho_banco
        load_dotenv()
    
    def cleanup_banco_robusto(self, callback=None):
        """Cleanup robusto do banco vetorial com retry logic"""
        if not os.path.exists(self.caminho_banco):
            return True
        
        if callback:
            callback("CLEANUP", "🧹 Iniciando limpeza robusta do banco vetorial...")
        
        # Força garbage collection para liberar recursos
        gc.collect()
        time.sleep(1)
        
        # Tenta fechar processos que podem estar usando os arquivos
        try:
            current_process = psutil.Process()
            for child in current_process.children(recursive=True):
                if 'chroma' in child.name().lower():
                    child.terminate()
            time.sleep(2)
        except Exception:
            pass
        
        # Retry logic para deletar o diretório
        max_tentativas = 5
        for tentativa in range(max_tentativas):
            try:
                if callback:
                    callback("CLEANUP", f"🔄 Tentativa {tentativa + 1}/{max_tentativas} de limpeza...")
                
                # Tenta remover atributos readonly primeiro
                for root, dirs, files in os.walk(self.caminho_banco):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            os.chmod(file_path, 0o777)
                        except Exception:
                            pass
                
                # Tenta deletar o diretório
                shutil.rmtree(self.caminho_banco, ignore_errors=True)
                
                # Verifica se foi deletado com sucesso
                if not os.path.exists(self.caminho_banco):
                    if callback:
                        callback("CLEANUP", "✅ Limpeza concluída com sucesso!")
                    return True
                
                # Se ainda existe, aguarda antes da próxima tentativa
                if tentativa < max_tentativas - 1:
                    delay = (tentativa + 1) * 2  # Backoff exponencial
                    if callback:
                        callback("CLEANUP", f"⏳ Aguardando {delay}s antes da próxima tentativa...")
                    time.sleep(delay)
                    gc.collect()  # Força garbage collection novamente
                    
            except Exception as e:
                if callback:
                    callback("CLEANUP", f"⚠️ Erro na tentativa {tentativa + 1}: {str(e)}")
                if tentativa < max_tentativas - 1:
                    time.sleep((tentativa + 1) * 2)
        
        # Se chegou aqui, não conseguiu deletar
        if callback:
            callback("ERRO", "❌ Não foi possível limpar o banco após múltiplas tentativas")
        return False
    
    def criar_banco_simples(self):
        """Cria banco vetorial de forma simples"""
        try:
            # Limpar banco antigo
            if os.path.exists(self.caminho_banco):
                shutil.rmtree(self.caminho_banco)
            
            # Carregar PDFs
            carregador = PyPDFDirectoryLoader(self.pasta_documentos)
            documentos = carregador.load()
            
            # Dividir em chunks
            divisor = RecursiveCharacterTextSplitter(
                chunk_size=TAMANHO_PEDACO,
                chunk_overlap=SOBREPOSICAO_PEDACO
            )
            chunks = divisor.split_documents(documentos)
            
            # Criar banco vetorial
            embeddings = OpenAIEmbeddings()
            Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=self.caminho_banco
            )
            
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False
    
    def criar_banco_com_progresso(self, callback=None):
        """Cria banco vetorial com callback de progresso detalhado"""
        try:
            if callback:
                callback("INICIO", "🚀 Iniciando criação do banco vetorial...")
            
            # Verificar se a pasta de documentos existe
            if not os.path.exists(self.pasta_documentos):
                erro_msg = f"❌ Pasta de documentos não encontrada: {self.pasta_documentos}"
                if callback:
                    callback("ERRO", erro_msg)
                print(erro_msg)
                return False
            
            # Verificar se há PDFs na pasta
            pdfs = [f for f in os.listdir(self.pasta_documentos) if f.lower().endswith('.pdf')]
            if not pdfs:
                erro_msg = f"❌ Nenhum arquivo PDF encontrado na pasta '{self.pasta_documentos}'!"
                if callback:
                    callback("ERRO", erro_msg)
                print(erro_msg)
                return False
            
            print(f"✅ Encontrados {len(pdfs)} arquivos PDF para processar")
            if callback:
                callback("DESCOBERTA", f"📁 Encontrados {len(pdfs)} arquivos PDF: {', '.join(pdfs[:3])}{'...' if len(pdfs) > 3 else ''}")
            
            # Limpar banco antigo com método robusto
            if not self.cleanup_banco_robusto(callback):
                erro_msg = "❌ Falha na limpeza do banco vetorial anterior!"
                if callback:
                    callback("ERRO", erro_msg)
                print(erro_msg)
                return False
            
            # Carregar documentos com detalhes
            if callback:
                callback("CARREGAMENTO", f"📖 Iniciando leitura de {len(pdfs)} documentos PDF...")
            
            try:
                carregador = PyPDFDirectoryLoader(self.pasta_documentos)
                documentos = carregador.load()
                
                if not documentos:
                    erro_msg = "❌ Nenhum conteúdo foi extraído dos PDFs!"
                    if callback:
                        callback("ERRO", erro_msg)
                    print(erro_msg)
                    return False
                
                # Mostrar detalhes dos arquivos processados
                arquivos_processados = {}
                for doc in documentos:
                    fonte = doc.metadata.get('source', 'Desconhecido')
                    nome_arquivo = os.path.basename(fonte)
                    if nome_arquivo not in arquivos_processados:
                        arquivos_processados[nome_arquivo] = 0
                    arquivos_processados[nome_arquivo] += 1
                
                detalhes_arquivos = []
                for arquivo, paginas in arquivos_processados.items():
                    detalhes_arquivos.append(f"📄 {arquivo} ({paginas} páginas)")
                
                print(f"✅ Carregados {len(documentos)} páginas de documentos")
                if callback:
                    callback("CARREGAMENTO_COMPLETO", f"✅ Processamento concluído:\n" + "\n".join(detalhes_arquivos))
                
            except Exception as e:
                erro_msg = f"❌ Erro ao carregar PDFs: {str(e)}"
                if callback:
                    callback("ERRO", erro_msg)
                print(erro_msg)
                return False
            
            # Dividir em chunks
            if callback:
                callback("DIVISAO", "Dividindo documentos em chunks")
            
            try:
                divisor = RecursiveCharacterTextSplitter(
                    chunk_size=TAMANHO_PEDACO,
                    chunk_overlap=SOBREPOSICAO_PEDACO
                )
                chunks = divisor.split_documents(documentos)
                
                if not chunks:
                    erro_msg = "❌ Nenhum chunk foi criado dos documentos!"
                    if callback:
                        callback("ERRO", erro_msg)
                    print(erro_msg)
                    return False
                    
                print(f"✅ Criados {len(chunks)} chunks de texto")
                
            except Exception as e:
                erro_msg = f"❌ Erro ao dividir documentos: {str(e)}"
                if callback:
                    callback("ERRO", erro_msg)
                print(erro_msg)
                return False
            
            # Criar embeddings
            if callback:
                callback("EMBEDDINGS", "Criando embeddings")
            
            try:
                embeddings = OpenAIEmbeddings()
                # Testar conexão com OpenAI
                teste_embedding = embeddings.embed_query("teste")
                print("✅ Conexão com OpenAI estabelecida")
                
            except Exception as e:
                erro_msg = f"❌ Erro ao conectar com OpenAI: {str(e)}"
                if callback:
                    callback("ERRO", erro_msg)
                print(erro_msg)
                return False
            
            # Criar banco vetorial com retry logic
            if callback:
                callback("BANCO", "🏗️ Criando banco vetorial...")
            
            max_tentativas_banco = 3
            for tentativa in range(max_tentativas_banco):
                try:
                    if tentativa > 0:
                        if callback:
                            callback("BANCO", f"🔄 Tentativa {tentativa + 1}/{max_tentativas_banco} de criação do banco...")
                        time.sleep(2)  # Aguarda antes de tentar novamente
                        gc.collect()  # Força garbage collection
                    
                    banco = Chroma.from_documents(
                        documents=chunks,
                        embedding=embeddings,
                        persist_directory=self.caminho_banco
                    )
                    
                    print(f"✅ Banco vetorial criado em '{self.caminho_banco}'")
                    if callback:
                        callback("BANCO", "✅ Banco vetorial criado com sucesso!")
                    break
                    
                except Exception as e:
                    erro_msg = f"❌ Erro na tentativa {tentativa + 1}: {str(e)}"
                    if callback:
                        callback("BANCO", erro_msg)
                    print(erro_msg)
                    
                    if tentativa == max_tentativas_banco - 1:
                        # Última tentativa falhou
                        erro_final = f"❌ Falha na criação do banco após {max_tentativas_banco} tentativas!"
                        if callback:
                            callback("ERRO", erro_final)
                        print(erro_final)
                        return False
                    
                    # Aguarda antes da próxima tentativa
                    time.sleep((tentativa + 1) * 3)
            else:
                return False
            
            if callback:
                callback("CONCLUIDO", "Banco criado com sucesso")
            
            print("🎉 Banco vetorial criado com sucesso!")
            return True
            
        except Exception as e:
            erro_msg = f"❌ Erro inesperado: {str(e)}"
            if callback:
                callback("ERRO", erro_msg)
            print(erro_msg)
            return False