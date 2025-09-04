import os
import streamlit as st
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from db_engine import MotorBanco
from config import *

class InterfaceStreamlit:
    """Interface simples para o Streamlit"""
    
    def __init__(self, caminho_banco):
        self.caminho_banco = caminho_banco
        self.motor_banco = MotorBanco(PASTA_BASE, caminho_banco)
    
    def mostrar_estatisticas_banco(self):
        """Mostra estatísticas básicas do banco"""
        if not os.path.exists(self.caminho_banco):
            st.warning("⚠️ Banco não encontrado")
            return
        
        try:
            banco = Chroma(persist_directory=self.caminho_banco, embedding_function=OpenAIEmbeddings())
            total = banco._collection.count()
            st.success(f"✅ Banco ativo com {total:,} chunks")
        except Exception as e:
            st.error(f"❌ Erro ao acessar banco: {str(e)}")
    
    def mostrar_gerenciamento_arquivos(self):
        """Interface simples para gerenciar arquivos PDF"""
        from config import PASTA_BASE
        import os
        
        st.markdown("### 📁 Gerenciar Arquivos PDF")
        
        # Upload simples
        arquivos = st.file_uploader("Adicionar PDFs:", type=['pdf'], accept_multiple_files=True)
        
        if arquivos and st.button("📥 Salvar", type="primary"):
            if not os.path.exists(PASTA_BASE):
                os.makedirs(PASTA_BASE)
            
            for arquivo in arquivos:
                with open(os.path.join(PASTA_BASE, arquivo.name), "wb") as f:
                    f.write(arquivo.getbuffer())
            
            st.success(f"✅ {len(arquivos)} arquivo(s) salvos!")
            st.rerun()
        
        # Lista simples de arquivos
        if os.path.exists(PASTA_BASE):
            pdfs = [f for f in os.listdir(PASTA_BASE) if f.endswith('.pdf')]
            if pdfs:
                st.info(f"📊 {len(pdfs)} arquivos encontrados")
                for pdf in pdfs:
                    col1, col2 = st.columns([4, 1])
                    col1.text(f"📄 {pdf}")
                    if col2.button("🗑️", key=f"del_{pdf}"):
                        os.remove(os.path.join(PASTA_BASE, pdf))
                        st.success(f"✅ {pdf} removido!")
                        st.rerun()
            else:
                st.warning("📂 Nenhum PDF encontrado")
        else:
            st.info("📂 Faça upload de arquivos para começar")
    
    def mostrar_interface_criacao_banco(self):
        """Interface simples para criar banco vetorial"""
        from config import validar_requisitos
        
        st.markdown("### 🚀 Criar Banco Vetorial")
        
        # Verificar se já está criando banco
        if 'criando_banco' not in st.session_state:
            st.session_state.criando_banco = False
        
        if st.session_state.criando_banco:
            st.warning("⏳ Criação em andamento... Aguarde!")
            return False
        
        # Verificar requisitos simples
        requisitos = validar_requisitos()
        
        for nome, status in requisitos.items():
            if status:
                st.success(f"✅ {nome.replace('_', ' ').title()}")
            else:
                st.error(f"❌ {nome.replace('_', ' ').title()}")
        
        # Botão de criação
        if all(requisitos.values()):
            if st.button("🚀 Criar Banco", type="primary", use_container_width=True):
                st.session_state.criando_banco = True
                with st.spinner("Criando banco..."):
                    sucesso = self._executar_criacao()
                
                st.session_state.criando_banco = False
                
                if sucesso:
                    st.success("✅ Banco criado com sucesso!")
                    if st.button("🏠 Ir para Chat", type="primary"):
                        st.session_state.menu_opcao = "🏠 Tela Principal"
                        st.rerun()
                return sucesso
        else:
            st.error("❌ Complete os requisitos acima")
        
        return False
    
    def mostrar_status_banco_completo(self):
        """Mostra status simples do banco"""
        import os
        
        st.markdown("### 📊 Status do Banco")
        
        if os.path.exists(self.caminho_banco):
            self.mostrar_estatisticas_banco()
        else:
            st.warning("⚠️ Banco não encontrado")
            st.info("Crie o banco na aba 'Criar Banco'")
    
    def _executar_criacao(self):
        """Executa criação do banco de forma simples"""
        barra = st.progress(0)
        status = st.empty()
        
        try:
            def callback(etapa, msg):
                progresso = {
                    "INICIO": 0.05, "DESCOBERTA": 0.1, "CLEANUP": 0.2, "LIMPEZA": 0.2,
                    "CARREGAMENTO": 0.3, "CARREGAMENTO_COMPLETO": 0.4, "DIVISAO": 0.5,
                    "EMBEDDINGS": 0.7, "BANCO": 0.8, "CONCLUIDO": 1.0
                }.get(etapa, 0.5)
                
                barra.progress(progresso)
                
                # Mostrar mensagens mais detalhadas
                if etapa == "ERRO":
                    status.error(f"❌ {msg}")
                elif etapa == "CLEANUP":
                    status.info(f"🧹 {msg}")
                elif etapa == "CARREGAMENTO_COMPLETO":
                    # Mostrar detalhes dos arquivos em uma área expansível
                    with st.expander("📄 Detalhes dos Arquivos Processados", expanded=False):
                        st.text(msg)
                    status.success("✅ Arquivos carregados com sucesso!")
                else:
                    status.text(f"🔄 {msg}")
            
            sucesso = self.motor_banco.criar_banco_com_progresso(callback)
            
            if sucesso:
                status.text("✅ Banco criado!")
                st.success("✨ Vá para a Tela Principal e teste!")
                return True
            else:
                status.text("❌ Erro na criação")
                st.error("❌ Falha na criação do banco")
                return False
        except Exception as e:
            status.text("❌ Erro")
            st.error(f"❌ Erro: {str(e)}")
            return False