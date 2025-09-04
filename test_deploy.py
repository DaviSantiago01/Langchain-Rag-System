#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste para Simular Deploy no Streamlit Cloud
Testa todas as importações e dependências críticas
"""

import sys
import os

def test_imports():
    """Testa todas as importações críticas"""
    print("🔍 Testando importações...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar Streamlit: {e}")
        return False
    
    try:
        import sqlite3
        print(f"✅ SQLite3 versão: {sqlite3.sqlite_version}")
        # Verifica se a versão é >= 3.35.0
        version_parts = [int(x) for x in sqlite3.sqlite_version.split('.')]
        if version_parts[0] > 3 or (version_parts[0] == 3 and version_parts[1] >= 35):
            print("✅ Versão SQLite3 compatível")
        else:
            print("⚠️ Versão SQLite3 pode ser incompatível")
    except ImportError as e:
        print(f"❌ Erro ao importar SQLite3: {e}")
        return False
    
    try:
        import chromadb
        print("✅ ChromaDB importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar ChromaDB: {e}")
        return False
    except RuntimeError as e:
        if "sqlite3" in str(e).lower():
            print(f"❌ Erro SQLite3 no ChromaDB: {e}")
            return False
        else:
            print(f"⚠️ Aviso ChromaDB: {e}")
    
    try:
        from langchain_community.document_loaders import PyPDFDirectoryLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_openai import OpenAIEmbeddings
        from langchain_chroma import Chroma
        from openai import OpenAI
        print("✅ Todas as dependências LangChain importadas")
    except ImportError as e:
        print(f"❌ Erro ao importar LangChain: {e}")
        return False
    
    try:
        from config import validar_api_key, PASTA_BASE, CAMINHO_BANCO
        print("✅ Config.py importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar config.py: {e}")
        return False
    
    try:
        from db_engine import buscar_resposta, verificar_banco_existe
        print("✅ db_engine.py importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar db_engine.py: {e}")
        return False
    
    try:
        from db_streamlit import mostrar_upload_interface, mostrar_lista_interface
        print("✅ db_streamlit.py importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar db_streamlit.py: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Testa funcionalidades básicas sem API key"""
    print("\n🔧 Testando funcionalidades básicas...")
    
    try:
        from db_engine import verificar_banco_existe
        existe = verificar_banco_existe()
        print(f"✅ Verificação de banco: {existe}")
    except Exception as e:
        print(f"❌ Erro na verificação de banco: {e}")
        return False
    
    try:
        from config import validar_api_key
        # Teste com chave inválida
        resultado = validar_api_key("teste_invalido")
        print(f"✅ Validação de API key (teste): {resultado}")
    except Exception as e:
        print(f"❌ Erro na validação de API key: {e}")
        return False
    
    return True

def main():
    """Função principal de teste"""
    print("🚀 TESTE DE DEPLOY - SIMULAÇÃO STREAMLIT CLOUD")
    print("=" * 50)
    print(f"Python: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    print("=" * 50)
    
    # Teste de importações
    if not test_imports():
        print("\n❌ FALHA: Problemas nas importações")
        return False
    
    # Teste de funcionalidades básicas
    if not test_basic_functionality():
        print("\n❌ FALHA: Problemas nas funcionalidades")
        return False
    
    print("\n✅ SUCESSO: Todos os testes passaram!")
    print("🚀 Pronto para deploy no Streamlit Cloud")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)