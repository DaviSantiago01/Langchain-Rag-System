import streamlit as st  # Streamlit = biblioteca para criar interfaces web
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

#Carregar variaveis de ambiente
load_dotenv()

#Configuçoes (Caminho do database)
CAMINHO_DB = "db"


# Template que será enviado para a IA junto com a pergunta e documentos
prompt_template = """ 
Analise os documentos abaixo e responda a pergunta do usuário.

PERGUNTA: {pergunta}

DOCUMENTOS:
{documentos}

INSTRUÇÕES:
- Use APENAS as informações dos documentos fornecidos
- Se a resposta estiver nos documentos, responda de forma clara e completa
- Se não encontrar informações suficientes, responda: "Não encontrei essa informação nos documentos fornecidos"
- Seja específico e cite as informações relevantes que encontrou
"""

def conectar_banco():
    """
    Esta função serve para:
    1. Conectar ao banco de dados uma única vez
    2. Verificar se tudo está funcionando
    3. Retornar o banco para uso posterior
    """
    try:
        funcao_embedding = OpenAIEmbeddings()  # Inicializar embeddings da OpenAI
        db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)  # Conectar ao banco
        return db
    except Exception as e:
        st.error(f"❌ Erro ao conectar banco: {e}")
        return None

def buscar_resposta(db, pergunta):
    """
    Esta função serve para:
    1. Buscar documentos relevantes no banco
    2. Filtrar por qualidade (relevância)
    3. Enviar para IA e retornar resposta
    """
    try:
        # Buscar documentos similares à pergunta
        resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)
        
        # Verificar se encontrou algo relevante (score mínimo de 0.5)
        if len(resultados) == 0 or resultados[0][1] < 0.5:
            return "❌ Não encontrei documentos relevantes para sua pergunta."
        
        # Extrair textos dos documentos encontrados
        textos_resultado = []
        for resultado in resultados:
            texto = resultado[0].page_content  # Pegar o texto do documento
            textos_resultado.append(texto)
        
        # Juntar todos os textos com separadores
        documentos = "\n\n----\n\n".join(textos_resultado)
        
        # Criar prompt estruturado para enviar à IA
        prompt = ChatPromptTemplate.from_template(prompt_template)
        prompt_formatado = prompt.invoke({"pergunta": pergunta, "documentos": documentos})
        
      # Enviar para IA e obter resposta
        modelo = ChatOpenAI(
            model="gpt-4o-mini",        # Modelo que existe e é bom
            temperature=1,            # Baixo = mais preciso (0.0 a 2.0)
            max_tokens=1000,           # Máximo de tokens na resposta
            timeout=30                 # Timeout em segundos
        )
        resposta = modelo.invoke(prompt_formatado)
        return resposta.content
        
    except Exception as e:
        return f"❌ Erro ao processar pergunta: {e}"

# ==============================================
# INTERFACE WEB COMEÇA AQUI
# ==============================================

def main():
    """
    Esta é a função principal da interface web
    """

    # Configurar página (título da aba, ícone, layout)
    st.set_page_config(
        page_title="Sistema de Perguntas e Respostas",
        page_icon="📚",
        layout="wide"
    )
    
    # Título principal da página
    st.title("📚 Sistema de Perguntas e Respostas")
    st.markdown("**Faça perguntas sobre seus documentos PDF!**")

     # Barra lateral com informações
    with st.sidebar:
        st.header("ℹ️ Como usar:")
        st.write("1. Certifique-se que o banco foi criado")
        st.write("2. Digite sua pergunta")
        st.write("3. Clique em 'Buscar Resposta'")
        st.write("4. Aguarde a resposta da IA")
        
        # Mostrar status do banco de dados
        if os.path.exists(CAMINHO_DB):
            st.success("✅ Banco de dados encontrado!")
        else:
            st.error("❌ Execute 'python criar_db.py' primeiro!")
    
    # Linha separadora
    st.markdown("---")
    
    # Verificar se banco de dados existe
    if not os.path.exists(CAMINHO_DB):
        st.error("🚨 **Banco de dados não encontrado!**")
        st.info("Execute o comando: `python criar_db.py` no terminal primeiro.")
        return  # Para o programa aqui se não tem banco
    
    # Conectar ao banco apenas uma vez (usando session_state para guardar na memória)
    if 'db' not in st.session_state:
        with st.spinner("🔄 Conectando ao banco de dados..."):  # Spinner = animação de carregamento
            st.session_state.db = conectar_banco()  # Guardar conexão na sessão
    
    # Verificar se conseguiu conectar
    if st.session_state.db is None:
        st.error("❌ Não foi possível conectar ao banco de dados!")
        return
    
    # Criar campo de entrada para pergunta
    pergunta = st.text_input(
        "🤔 Sua pergunta:",
        placeholder="Ex: Qual é o tema principal do documento?",
        help="Digite sua pergunta sobre os documentos PDF"
    )
    
    # Criar botão para buscar resposta
    botao_buscar = st.button("🔍 Buscar Resposta", type="primary")
    
    # Processar quando clicar no botão
    if botao_buscar:
        if pergunta.strip():  # Verificar se pergunta não está vazia
            
            # Mostrar a pergunta do usuário
            st.markdown("### 📝 Sua pergunta:")
            st.info(pergunta)
            
            # Buscar resposta com animação de carregamento
            with st.spinner("🤖 IA analisando documentos..."):
                resposta = buscar_resposta(st.session_state.db, pergunta)
            
            # Mostrar resposta
            st.markdown("### 🤖 Resposta:")
            
            if resposta.startswith("❌"):  # Se deu erro
                st.error(resposta)
            else:  # Se deu certo
                st.success("✅ Resposta encontrada!")
                st.markdown(resposta)
            
        else:
            st.warning("⚠️ Por favor, digite uma pergunta!")
    
    # Rodapé com dica
    st.markdown("---")
    st.markdown("💡 **Dica:** Faça perguntas específicas para obter melhores respostas!")

# Executar a aplicação
if __name__ == "__main__":
    main()