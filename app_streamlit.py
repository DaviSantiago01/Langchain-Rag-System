import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from db_streamlit import InterfaceStreamlit
from config import *

def conectar_banco_vetorial():
    if not os.path.exists(CAMINHO_BANCO):
        st.error("❌ Banco vetorial não encontrado! Crie o banco primeiro na aba 'Criar Banco'.")
        return None
    
    try:
        # Usar API key ativa (usuário ou padrão)
        api_key = obter_api_key_ativa()
        embeddings = OpenAIEmbeddings(api_key=api_key)
        return Chroma(
            persist_directory=CAMINHO_BANCO,
            embedding_function=embeddings
        )
    except Exception as e:
        st.error(f"❌ Erro ao conectar banco: {str(e)}")
        return None

def buscar_resposta(pergunta: str, banco_vetorial):
    """Busca resposta usando RAG com configurações personalizadas"""
    if not banco_vetorial or not pergunta.strip():
        return "❌ Erro: banco ou pergunta inválidos"
    
    try:
        # Usar configurações ativas (usuário ou padrão)
        api_key = obter_api_key_ativa()
        modelo = obter_modelo_ativo()
        temperatura = obter_temperatura_ativa()
        max_tokens = obter_max_tokens_ativo()
        timeout = obter_timeout_ativo()
        
        # Criar LLM com configurações personalizadas
        llm = ChatOpenAI(
            model=modelo,
            temperature=temperatura,
            max_tokens=max_tokens,
            timeout=timeout,
            api_key=api_key
        )
        
        # Buscar documentos relevantes
        docs = banco_vetorial.similarity_search(pergunta, k=RESULTADOS_BUSCA)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Criar prompt simples
        prompt = f"Contexto: {context}\n\nPergunta: {pergunta}\n\nResposta:"
        
        # Gerar resposta
        resposta = llm.invoke(prompt)
        return resposta.content if hasattr(resposta, 'content') else str(resposta)
        
    except Exception as e:
        return f"❌ Erro: {str(e)}"

def mostrar_tela_principal():
    """Tela principal - Chat RAG simples"""
    st.markdown("### 🤖 Chat RAG")
    
    banco = conectar_banco_vetorial()
    
    if not banco:
        st.warning("⚠️ Banco não encontrado")
        st.info("💡 Vá para **🗄️ Configurar Banco** para criar o banco")
        
        if st.button("🗄️ Configurar Banco", type="primary"):
            st.session_state.menu_opcao = "🗄️ Configurar Banco"
            st.rerun()
        return
    
    try:
        total = banco._collection.count()
        # Sistema funcionando normalmente - interface limpa
    except:
        st.error("❌ Erro: Banco de dados não está funcionando corretamente. Verifique a configuração.")
    
    # Interface de chat simples
    pergunta = st.text_area("💭 Sua pergunta:", placeholder="Digite sua pergunta...", height=80)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        buscar = st.button("🔍 Buscar", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.rerun()
    
    if buscar and pergunta.strip():
        with st.spinner("🔍 Buscando..."):
            resposta = buscar_resposta(pergunta, banco)
        
        st.markdown("### 💡 Resposta")
        st.markdown(resposta)
    
    elif buscar:
        st.warning("⚠️ Digite uma pergunta")

def mostrar_configuracao_sistema():
    """Tela avançada de configuração do sistema"""
    st.markdown("### ⚙️ Configuração do Sistema")
    
    # Informações básicas do sistema
    with st.expander("📋 Informações do Sistema", expanded=False):
        st.info(f"📁 **Pasta Base:** {PASTA_BASE}")
        st.info(f"🗄️ **Banco:** {CAMINHO_BANCO}")
    
    st.markdown("---")
    st.markdown("### 🔧 Configurações Personalizadas")
    
    # Configurações do usuário
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Obter configurações atuais
        config_atual = obter_configuracoes_usuario()
        
        # API Key
        st.markdown("#### 🔑 Chave OpenAI")
        api_key_atual = config_atual["api_key"]
        api_key_placeholder = "sk-..." if api_key_atual else "Cole sua API key aqui"
        
        nova_api_key = st.text_input(
            "API Key:",
            value=api_key_atual,
            placeholder=api_key_placeholder,
            type="password",
            help="Sua chave de API do OpenAI para usar os modelos de IA"
        )
        
        # Modelo
        st.markdown("#### 🤖 Modelo de IA")
        modelos_disponiveis = [
            "gpt-4o-mini",
            "gpt-4o", 
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
        
        modelo_atual = config_atual["modelo"]
        if modelo_atual not in modelos_disponiveis:
            modelos_disponiveis.append(modelo_atual)
        
        novo_modelo = st.selectbox(
            "Escolha o modelo:",
            modelos_disponiveis,
            index=modelos_disponiveis.index(modelo_atual),
            help="Modelo de IA que será usado para responder perguntas"
        )
        
        # Temperatura
        st.markdown("#### 🌡️ Temperatura")
        nova_temperatura = st.slider(
            "Criatividade das respostas:",
            min_value=0.0,
            max_value=1.0,
            value=config_atual["temperatura"],
            step=0.1,
            help="0.0 = Respostas mais precisas | 1.0 = Respostas mais criativas"
        )
        
        # Configurações avançadas
        with st.expander("⚙️ Configurações Avançadas", expanded=False):
            novo_max_tokens = st.number_input(
                "Máximo de tokens:",
                min_value=100,
                max_value=4000,
                value=config_atual["max_tokens"],
                step=100,
                help="Tamanho máximo das respostas"
            )
            
            novo_timeout = st.number_input(
                "Timeout (segundos):",
                min_value=10,
                max_value=120,
                value=config_atual["timeout"],
                step=5,
                help="Tempo limite para respostas da IA"
            )
    
    with col2:
        st.markdown("#### 📊 Status")
        
        # Validação das configurações
        if nova_api_key != api_key_atual:
            if validar_api_key(nova_api_key):
                st.success("✅ API Key válida")
            else:
                st.error("❌ API Key inválida")
        else:
            if validar_api_key(api_key_atual):
                st.success("✅ API Key configurada")
            else:
                st.error("❌ API Key não configurada")
        
        if novo_modelo:
            st.success(f"✅ Modelo: {novo_modelo}")
        
        if 0.0 <= nova_temperatura <= 1.0:
            st.success(f"✅ Temperatura: {nova_temperatura}")
        
        # Verificar requisitos do sistema
        st.markdown("#### 🔍 Requisitos")
        requisitos = validar_requisitos()
        
        if requisitos['pasta_base']:
            st.success("✅ Pasta base OK")
        else:
            st.error("❌ Pasta base não encontrada")
        
        if requisitos['arquivos_pdf']:
            st.success("✅ PDFs encontrados")
        else:
            st.warning("⚠️ Nenhum PDF encontrado")
    
    # Botões de ação
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Salvar Configurações", type="primary", use_container_width=True):
            # Salvar todas as configurações
            atualizar_configuracao_usuario("api_key", nova_api_key)
            atualizar_configuracao_usuario("modelo", novo_modelo)
            atualizar_configuracao_usuario("temperatura", nova_temperatura)
            atualizar_configuracao_usuario("max_tokens", novo_max_tokens)
            atualizar_configuracao_usuario("timeout", novo_timeout)
            
            st.success("✅ Configurações salvas com sucesso!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Resetar Padrões", use_container_width=True):
            resetar_configuracoes_usuario()
            st.success("✅ Configurações resetadas!")
            st.rerun()
    
    with col3:
        if st.button("🧪 Testar API", use_container_width=True):
            if validar_api_key(nova_api_key):
                st.success("✅ API funcionando!")
            else:
                st.error("❌ Erro na API")

def mostrar_configuracao_banco():
    """Tela de configuração do banco"""
    st.markdown("## 🗄️ Configurar Banco")
    
    # Verificar se há API key configurada
    api_key_disponivel = obter_api_key_ativa()
    
    if not api_key_disponivel:
        st.error("🔑 Chave OpenAI não configurada!")
        st.info("💡 Configure sua API key na aba **⚙️ Configurar Sistema**")
        if st.button("⚙️ Ir para Configurações", type="primary"):
            st.session_state.menu_opcao = "⚙️ Configurar Sistema"
            st.rerun()
        return
    
    # Cache da interface para evitar múltiplas instâncias
    if 'interface_streamlit' not in st.session_state:
        st.session_state.interface_streamlit = InterfaceStreamlit(CAMINHO_BANCO)
    
    interface = st.session_state.interface_streamlit
    
    tab1, tab2, tab3 = st.tabs(["📁 Arquivos", "🚀 Criar", "📊 Status"])
    
    with tab1:
        interface.mostrar_gerenciamento_arquivos()
    with tab2:
        interface.mostrar_interface_criacao_banco()
    with tab3:
        interface.mostrar_status_banco_completo()

def main():
    """Função principal do aplicativo"""
    st.set_page_config(page_title="RAG System", page_icon="🤖", layout="wide")
    
    st.title("🤖 Sistema RAG Avançado")
    st.markdown("Faça perguntas sobre seus documentos PDF com configurações personalizáveis")
    
    with st.sidebar:
        st.markdown("### 📋 Menu")
        
        # Controle de navegação
        if 'menu_opcao' not in st.session_state:
            st.session_state.menu_opcao = "🏠 Tela Principal"
        
        opcoes = ["🏠 Tela Principal", "🗄️ Configurar Banco", "⚙️ Configurar Sistema"]
        opcao_selecionada = st.radio("Escolha:", opcoes, index=opcoes.index(st.session_state.menu_opcao))
        
        if opcao_selecionada != st.session_state.menu_opcao:
            st.session_state.menu_opcao = opcao_selecionada
            st.rerun()
        
        st.markdown("---")
        st.info("**Sistema RAG Avançado**\nPerguntas sobre PDFs usando IA com configurações personalizáveis")
        
        # Configurações atuais em expander
        with st.expander("🔧 Configurações Atuais", expanded=False):
            st.info(f"🤖 **Modelo:** {obter_modelo_ativo()}")
            st.info(f"🌡️ **Temperatura:** {obter_temperatura_ativa()}")
            config_atual = obter_configuracoes_usuario()
            api_status = "✅ Personalizada" if config_atual["api_key"] else "🔄 Padrão"
            st.info(f"🔑 **API:** {api_status}")
    
    if opcao_selecionada == "🏠 Tela Principal":
        mostrar_tela_principal()
    elif opcao_selecionada == "🗄️ Configurar Banco":
        mostrar_configuracao_banco()
    else:
        mostrar_configuracao_sistema()

if __name__ == "__main__":
    main()