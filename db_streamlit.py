# -*- coding: utf-8 -*-
"""
Interface Streamlit para Banco Vetorial - Versão Educacional Simplificada
Apenas 3 funções essenciais para iniciantes em Python
"""

import os
import streamlit as st
from db_engine import criar_banco_vetorial, listar_documentos
from config import PASTA_BASE

# =============================================================================
# FUNÇÕES DE INTERFACE - VERSÃO EDUCACIONAL SIMPLIFICADA
# =============================================================================

def mostrar_upload_interface():
    """
    Interface simplificada para upload de arquivos PDF.
    Função educacional para iniciantes.
    """
    st.subheader("📁 Upload de Documentos")
    
    # Upload de arquivos
    arquivos_enviados = st.file_uploader(
        "Selecione arquivos PDF:",
        type=['pdf'],
        accept_multiple_files=True,
        help="Escolha um ou mais arquivos PDF para análise"
    )
    
    if arquivos_enviados:
        # Criar pasta se não existir
        if not os.path.exists(PASTA_BASE):
            os.makedirs(PASTA_BASE)
        
        # Salvar arquivos
        if st.button("💾 Salvar Arquivos", type="primary"):
            try:
                for arquivo in arquivos_enviados:
                    caminho_arquivo = os.path.join(PASTA_BASE, arquivo.name)
                    with open(caminho_arquivo, "wb") as f:
                        f.write(arquivo.getbuffer())
                
                st.success(f"✅ {len(arquivos_enviados)} arquivo(s) salvos com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar arquivos: {str(e)}")


def mostrar_lista_interface():
    """
    Interface simplificada para listar e remover documentos.
    Função educacional para iniciantes.
    """
    st.subheader("📋 Documentos Salvos")
    
    # Listar documentos
    documentos = listar_documentos()
    
    if not documentos:
        st.info("📝 Nenhum documento encontrado. Faça upload de arquivos PDF primeiro.")
        return
    
    st.write(f"**Total de documentos:** {len(documentos)}")
    
    # Mostrar lista de documentos
    for i, doc in enumerate(documentos):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"📄 {doc}")
        
        with col2:
            if st.button("🗑️ Remover", key=f"remove_{i}"):
                try:
                    caminho_arquivo = os.path.join(PASTA_BASE, doc)
                    if os.path.exists(caminho_arquivo):
                        os.remove(caminho_arquivo)
                        st.success(f"✅ {doc} removido com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"❌ Arquivo {doc} não encontrado.")
                except Exception as e:
                    st.error(f"❌ Erro ao remover {doc}: {str(e)}")


def mostrar_criar_banco_interface(api_key):
    """
    Interface simplificada para criar o banco vetorial.
    Função educacional para iniciantes.
    
    Args:
        api_key (str): Chave da API da OpenAI
    """
    st.subheader("🏗️ Criar Banco Vetorial")
    
    # Verificar se há documentos
    documentos = listar_documentos()
    
    if not documentos:
        st.warning("⚠️ Nenhum documento encontrado. Faça upload de PDFs primeiro.")
        return
    
    # Verificar API key
    if not api_key:
        st.warning("⚠️ Configure sua chave da API OpenAI primeiro.")
        return
    
    # Mostrar informações
    st.info(f"📊 {len(documentos)} documento(s) pronto(s) para processamento")
    
    # Botão para criar banco
    if st.button("🚀 Criar Banco Vetorial", type="primary"):
        with st.spinner("Processando documentos... Isso pode levar alguns minutos."):
            try:
                sucesso = criar_banco_vetorial(api_key)
                
                if sucesso:
                    st.success("🎉 Banco vetorial criado com sucesso!")
                    st.balloons()
                else:
                    st.error("❌ Erro ao criar banco vetorial. Verifique os documentos e tente novamente.")
                    
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")