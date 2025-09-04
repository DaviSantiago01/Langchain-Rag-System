# -*- coding: utf-8 -*-
"""
Configuração Básica para RAG Educacional
Versão simplificada para iniciantes em Python
"""

import os

# =============================================================================
# CONSTANTES ESSENCIAIS
# =============================================================================

# Pasta onde os arquivos PDF serão armazenados
PASTA_BASE = "base"

# Nome do banco de dados vetorial
NOME_BANCO = "banco_vetorial"

# Caminho completo do banco vetorial
CAMINHO_BANCO = os.path.join(PASTA_BASE, NOME_BANCO)

# Configurações para divisão de texto
TAMANHO_PEDACO = 1000  # Tamanho de cada pedaço de texto
SOBREPOSICAO_PEDACO = 200  # Sobreposição entre pedaços

# Modelo da OpenAI (fixo para simplicidade)
MODELO_OPENAI = "gpt-3.5-turbo"

# =============================================================================
# FUNÇÃO BÁSICA
# =============================================================================

def validar_api_key(api_key):
    """
    Valida se a chave da API OpenAI está no formato correto.
    Função simples para iniciantes.
    
    Args:
        api_key (str): Chave da API para validar
        
    Returns:
        bool: True se válida, False se inválida
    """
    if not api_key:
        return False
    
    # Chave OpenAI deve começar com 'sk-' e ter pelo menos 20 caracteres
    return api_key.startswith('sk-') and len(api_key) >= 20