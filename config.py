from dotenv import load_dotenv
import os
import json
from pathlib import Path
from typing import Dict, Any

# Configurações básicas do sistema
PASTA_BASE = "base"
CAMINHO_BANCO = "chroma_db"

# Configurações de chunking
TAMANHO_PEDACO = 1000
SOBREPOSICAO_PEDACO = 200
SEPARADORES_TEXTO = ["\n\n", "\n", " ", ""]

# Configurações de busca
RESULTADOS_BUSCA = 3

# Configurações padrão do modelo (usadas se usuário não personalizar)
TEMPERATURA_PADRAO = 0.1
MAX_TOKENS_PADRAO = 1000
TIMEOUT_PADRAO = 30
NOME_MODELO_PADRAO = "gpt-4o-mini"

RESULTADOS_TESTE = 1
TAMANHO_PREVIEW = 100

ETAPAS_PROGRESSO = {
    'PASTA': (0.2, '📁 Verificando pasta base...'),
    'DOCS': (0.4, '📖 Carregando documentos...'),
    'SPLIT': (0.6, '✂️ Dividindo em chunks...'),
    'AI': (0.8, '🧠 Criando embeddings...'),
    'OK': (0.9, '💾 Salvando no banco...'),
    'TESTE': (0.95, '🧪 Testando banco...')
}

TEMPLATE_RESPOSTA = """
Analise os documentos e responda a pergunta de forma educativa.

PERGUNTA: {pergunta}

DOCUMENTOS:
{documentos}

INSTRUÇÕES:
- Use APENAS informações dos documentos fornecidos
- Se a resposta estiver nos documentos, responda de forma clara
- Se não houver informação suficiente, responda: "Não encontrei essa informação nos documentos"
- Seja específico e didático
"""

# Arquivo de configurações do usuário
ARQUIVO_CONFIG_USUARIO = "config_usuario.json"

def obter_configuracoes_usuario() -> Dict[str, Any]:
    """Obtém configurações personalizadas do usuário ou retorna padrões"""
    configuracoes_padrao = {
        "api_key": "",
        "modelo": NOME_MODELO_PADRAO,
        "temperatura": TEMPERATURA_PADRAO,
        "max_tokens": MAX_TOKENS_PADRAO,
        "timeout": TIMEOUT_PADRAO
    }
    
    if os.path.exists(ARQUIVO_CONFIG_USUARIO):
        try:
            with open(ARQUIVO_CONFIG_USUARIO, 'r', encoding='utf-8') as f:
                config_usuario = json.load(f)
            # Mescla com padrões para garantir que todas as chaves existam
            configuracoes_completas = configuracoes_padrao.copy()
            configuracoes_completas.update(config_usuario)
            return configuracoes_completas
        except Exception:
            return configuracoes_padrao
    
    return configuracoes_padrao

def salvar_configuracoes_usuario(configuracoes: Dict[str, Any]) -> bool:
    """Salva configurações personalizadas do usuário"""
    try:
        with open(ARQUIVO_CONFIG_USUARIO, 'w', encoding='utf-8') as f:
            json.dump(configuracoes, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def atualizar_configuracao_usuario(chave: str, valor: Any) -> bool:
    """Atualiza uma configuração específica do usuário"""
    configuracoes = obter_configuracoes_usuario()
    configuracoes[chave] = valor
    return salvar_configuracoes_usuario(configuracoes)

def resetar_configuracoes_usuario() -> bool:
    """Reseta configurações do usuário para os padrões"""
    configuracoes_padrao = {
        "api_key": "",
        "modelo": NOME_MODELO_PADRAO,
        "temperatura": TEMPERATURA_PADRAO,
        "max_tokens": MAX_TOKENS_PADRAO,
        "timeout": TIMEOUT_PADRAO
    }
    return salvar_configuracoes_usuario(configuracoes_padrao)

def validar_api_key(api_key: str) -> bool:
    """Valida se a API key do OpenAI é válida"""
    if not api_key or len(api_key) < 20:
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        client.models.list()
        return True
    except Exception:
        return False

def obter_api_key_ativa() -> str:
    """Obtém a API key ativa (usuário ou padrão do ambiente)"""
    config_usuario = obter_configuracoes_usuario()
    return config_usuario["api_key"] if config_usuario["api_key"] else os.getenv('OPENAI_API_KEY', '')

def obter_modelo_ativo() -> str:
    """Obtém o modelo ativo (usuário ou padrão)"""
    config_usuario = obter_configuracoes_usuario()
    return config_usuario["modelo"]

def obter_temperatura_ativa() -> float:
    """Obtém a temperatura ativa (usuário ou padrão)"""
    config_usuario = obter_configuracoes_usuario()
    return config_usuario["temperatura"]

def obter_max_tokens_ativo() -> int:
    """Obtém o max_tokens ativo (usuário ou padrão)"""
    config_usuario = obter_configuracoes_usuario()
    return config_usuario["max_tokens"]

def obter_timeout_ativo() -> int:
    """Obtém o timeout ativo (usuário ou padrão)"""
    config_usuario = obter_configuracoes_usuario()
    return config_usuario["timeout"]

def validar_requisitos():
    load_dotenv()  # Carrega variáveis do arquivo .env
    pasta_existe = os.path.exists(PASTA_BASE)
    pdfs_existem = False
    
    if pasta_existe:
        pdfs = [f for f in os.listdir(PASTA_BASE) if f.lower().endswith('.pdf')]
        pdfs_existem = len(pdfs) > 0
    
    return {
        'chave_openai': bool(obter_api_key_ativa()),
        'pasta_base': pasta_existe,
        'arquivos_pdf': pdfs_existem
    }

# Manter compatibilidade com código existente
TEMPERATURA = obter_temperatura_ativa()
MAX_TOKENS = obter_max_tokens_ativo()
TIMEOUT = obter_timeout_ativo()
NOME_MODELO = obter_modelo_ativo()