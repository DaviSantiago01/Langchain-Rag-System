# -*- coding: utf-8 -*-
"""
Aplicação RAG Educacional - Versão Simplificada
Apenas 3 telas básicas para iniciantes em Python
"""

import streamlit as st

# Tratamento de importações com mensagens de erro claras
try:
    from db_engine import buscar_resposta, verificar_banco_existe
    from db_streamlit import mostrar_upload_interface, mostrar_lista_interface, mostrar_criar_banco_interface
    from config import validar_api_key
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {str(e)}")
    st.error("Verifique se todos os arquivos estão presentes: config.py, db_engine.py, db_streamlit.py")
    st.stop()

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================

st.set_page_config(
    page_title="RAG Educacional",
    page_icon="🤖",
    layout="wide"
)

# =============================================================================
# FUNÇÕES PRINCIPAIS - VERSÃO EDUCACIONAL SIMPLIFICADA
# =============================================================================

def mostrar_tela_chat():
    """
    Tela principal de chat com o sistema RAG.
    Função educacional simplificada.
    """
    st.title("🤖 Chat RAG Educacional")
    
    # Verificar API key
    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.warning("⚠️ Configure sua chave da API OpenAI primeiro.")
        st.info("👈 Use o menu lateral para configurar.")
        return
    
    # Verificar se banco existe
    if not verificar_banco_existe():
        st.warning("⚠️ Banco vetorial não encontrado.")
        st.info("👈 Use o menu lateral para fazer upload e criar o banco.")
        return
    
    # Interface de chat
    st.success("✅ Sistema pronto! Faça sua pergunta abaixo:")
    
    # Campo de pergunta
    pergunta = st.text_input(
        "Digite sua pergunta:",
        placeholder="Ex: Qual é o tema principal dos documentos?",
        help="Faça perguntas sobre o conteúdo dos documentos enviados"
    )
    
    # Botão para enviar pergunta
    if st.button("🚀 Enviar Pergunta", type="primary") and pergunta:
        with st.spinner("Buscando resposta..."):
            resposta = buscar_resposta(pergunta, st.session_state.api_key)
            
            # Mostrar resposta
            st.markdown("### 💬 Resposta:")
            st.markdown(resposta)


def mostrar_tela_upload():
    """
    Tela para gerenciar documentos e criar banco vetorial.
    Função educacional simplificada.
    """
    st.title("📁 Gerenciar Documentos")
    
    # Verificar API key
    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.warning("⚠️ Configure sua chave da API OpenAI primeiro.")
        st.info("👈 Use o menu lateral para configurar.")
        return
    
    # Abas para organizar funcionalidades
    tab1, tab2, tab3 = st.tabs(["📤 Upload", "📋 Lista", "🏗️ Criar Banco"])
    
    with tab1:
        mostrar_upload_interface()
    
    with tab2:
        mostrar_lista_interface()
    
    with tab3:
        mostrar_criar_banco_interface(st.session_state.api_key)


def mostrar_tela_config():
    """
    Tela simples para configurar a API key.
    Função educacional simplificada.
    """
    st.title("⚙️ Configurações")
    
    st.markdown("### 🔑 Chave da API OpenAI")
    
    # Campo para API key
    api_key_input = st.text_input(
        "Digite sua chave da API:",
        type="password",
        placeholder="sk-...",
        help="Obtenha sua chave em: https://platform.openai.com/api-keys"
    )
    
    # Botão para salvar
    if st.button("💾 Salvar Configuração", type="primary"):
        if api_key_input:
            if validar_api_key(api_key_input):
                st.session_state.api_key = api_key_input
                st.success("✅ Chave da API configurada com sucesso!")
                st.rerun()
            else:
                st.error("❌ Chave da API inválida. Verifique e tente novamente.")
        else:
            st.error("❌ Digite uma chave da API válida.")
    
    # Mostrar status atual
    if "api_key" in st.session_state and st.session_state.api_key:
        st.success("✅ API key configurada")
        
        if st.button("🗑️ Remover Configuração"):
            del st.session_state.api_key
            st.success("✅ Configuração removida!")
            st.rerun()
    else:
        st.info("ℹ️ Nenhuma API key configurada")


# =============================================================================
# APLICAÇÃO PRINCIPAL
# =============================================================================

def main():
    """
    Função principal da aplicação.
    Controla a navegação entre as telas.
    """
    # Menu lateral
    with st.sidebar:
        st.title("🎯 Menu")
        
        # Opções de navegação
        opcao = st.radio(
            "Escolha uma opção:",
            ["🤖 Chat", "📁 Documentos", "⚙️ Configurações"],
            help="Navegue entre as diferentes funcionalidades"
        )
        
        # Separador
        st.divider()
        
        # Informações básicas
        st.markdown("### ℹ️ Sobre")
        st.info(
            "Sistema RAG educacional para\n"
            "aprender Python e IA.\n\n"
            "**Passos:**\n"
            "1. Configure a API\n"
            "2. Faça upload de PDFs\n"
            "3. Crie o banco vetorial\n"
            "4. Faça perguntas!"
        )
    
    # Mostrar tela selecionada
    if opcao == "🤖 Chat":
        mostrar_tela_chat()
    elif opcao == "📁 Documentos":
        mostrar_tela_upload()
    elif opcao == "⚙️ Configurações":
        mostrar_tela_config()


# =============================================================================
# EXECUÇÃO DA APLICAÇÃO
# =============================================================================

if __name__ == "__main__":
    main()