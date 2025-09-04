# -*- coding: utf-8 -*-
"""
Operações de Banco Vetorial - Versão Educacional Simplificada
Apenas funções essenciais para iniciantes em Python
"""

import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from openai import OpenAI
from config import PASTA_BASE, CAMINHO_BANCO, TAMANHO_PEDACO, SOBREPOSICAO_PEDACO, MODELO_OPENAI

# =============================================================================
# FUNÇÕES PRINCIPAIS - VERSÃO EDUCACIONAL SIMPLIFICADA
# =============================================================================

def criar_banco_vetorial(api_key):
    """
    Cria o banco vetorial completo a partir dos PDFs.
    Função simplificada para iniciantes.
    
    Args:
        api_key (str): Chave da API da OpenAI
    
    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        # Verificar se há PDFs
        if not os.path.exists(PASTA_BASE):
            return False
        
        pdfs = [f for f in os.listdir(PASTA_BASE) if f.lower().endswith('.pdf')]
        if not pdfs:
            return False
        
        # Limpar banco antigo
        if os.path.exists(CAMINHO_BANCO):
            shutil.rmtree(CAMINHO_BANCO)
        
        # Carregar documentos
        carregador = PyPDFDirectoryLoader(PASTA_BASE)
        documentos = carregador.load()
        
        if not documentos:
            return False
        
        # Dividir em pedaços
        divisor = RecursiveCharacterTextSplitter(
            chunk_size=TAMANHO_PEDACO,
            chunk_overlap=SOBREPOSICAO_PEDACO
        )
        pedacos = divisor.split_documents(documentos)
        
        if not pedacos:
            return False
        
        # Criar banco vetorial
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        Chroma.from_documents(
            documents=pedacos,
            embedding=embeddings,
            persist_directory=CAMINHO_BANCO
        )
        
        return True
        
    except Exception:
        return False


def buscar_resposta(pergunta, api_key):
    """
    Busca uma resposta no banco vetorial para a pergunta do usuário.
    Função simplificada para iniciantes.
    
    Args:
        pergunta (str): Pergunta do usuário
        api_key (str): Chave da API da OpenAI
    
    Returns:
        str: Resposta encontrada ou mensagem de erro
    """
    try:
        # Verificar se o banco existe
        if not os.path.exists(CAMINHO_BANCO):
            return "❌ Banco vetorial não encontrado. Crie o banco primeiro."
        
        # Carregar o banco vetorial
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        banco = Chroma(persist_directory=CAMINHO_BANCO, embedding_function=embeddings)
        
        # Buscar documentos similares
        docs_similares = banco.similarity_search(pergunta, k=3)
        
        if not docs_similares:
            return "❌ Nenhum documento similar encontrado."
        
        # Preparar contexto
        contexto = "\n\n".join([doc.page_content for doc in docs_similares])
        
        # Criar prompt
        prompt = f"""Baseado no contexto abaixo, responda a pergunta de forma clara e objetiva.
        
Contexto:
{contexto}
        
Pergunta: {pergunta}
        
Resposta:"""
        
        # Usar OpenAI para gerar resposta
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=MODELO_OPENAI,
            messages=[
                {"role": "system", "content": "Você é um assistente útil que responde perguntas baseado no contexto fornecido."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Erro ao processar pergunta: {str(e)}"


def listar_documentos():
    """
    Lista todos os documentos PDF disponíveis na pasta base.
    Função simplificada para iniciantes.
    
    Returns:
        list: Lista com nomes dos arquivos PDF
    """
    try:
        if not os.path.exists(PASTA_BASE):
            return []
        
        pdfs = [f for f in os.listdir(PASTA_BASE) if f.lower().endswith('.pdf')]
        return pdfs
        
    except Exception:
        return []


def verificar_banco_existe():
    """
    Verifica se o banco vetorial já foi criado.
    Função simplificada para iniciantes.
    
    Returns:
        bool: True se o banco existe, False caso contrário
    """
    try:
        return os.path.exists(CAMINHO_BANCO) and os.listdir(CAMINHO_BANCO)
    except Exception:
        return False