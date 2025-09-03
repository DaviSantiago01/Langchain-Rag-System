import streamlit as st
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = "chroma_db"

PROMPT_TEMPLATE = """ 
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

def conectar_database():
    try:
        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        return db
    except Exception as e:
        st.error(f"❌ Erro ao conectar banco: {e}")
        return None

def buscar_resposta(db, pergunta):
    try:
        resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)
        
        if len(resultados) == 0 or resultados[0][1] < 0.5:
            return "❌ Não encontrei documentos relevantes para sua pergunta."
        
        textos_documentos = [resultado[0].page_content for resultado in resultados]
        documentos = "\n\n----\n\n".join(textos_documentos)
        
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt_formatado = prompt.invoke({"pergunta": pergunta, "documentos": documentos})
        
        modelo = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=1000,
            timeout=30
        )
        resposta = modelo.invoke(prompt_formatado)
        return resposta.content
        
    except Exception as e:
        return f"❌ Erro ao processar pergunta: {e}"

def exibir_tela_principal():
    """Exibe a tela principal do sistema de perguntas e respostas"""
    st.markdown("---")
    
    if not os.path.exists(DB_PATH):
        st.error("🚨 **Banco de dados não encontrado!**")
        st.info("Execute o comando: `python criar_db.py` no terminal primeiro.")
        return
    
    if 'db' not in st.session_state:
        with st.spinner("🔄 Conectando ao banco de dados..."):
            st.session_state.db = conectar_database()
    
    if st.session_state.db is None:
        st.error("❌ Não foi possível conectar ao banco de dados!")
        return
    
    pergunta = st.text_input(
        "🤔 Sua pergunta:",
        placeholder="Ex: Qual é o tema principal do documento?",
        help="Digite sua pergunta sobre os documentos PDF"
    )
    
    botao_buscar = st.button("🔍 Buscar Resposta", type="primary")
    
    if botao_buscar:
        if pergunta.strip():
            st.markdown("### 📝 Sua pergunta:")
            st.info(pergunta)
            
            with st.spinner("🤖 IA analisando documentos..."):
                resposta = buscar_resposta(st.session_state.db, pergunta)
            
            st.markdown("### 🤖 Resposta:")
            
            if resposta.startswith("❌"):
                st.error(resposta)
            else:
                st.success("✅ Resposta encontrada!")
                st.markdown(resposta)
                
        else:
            st.warning("⚠️ Por favor, digite uma pergunta!")
    
    st.markdown("---")
    st.markdown("💡 **Dica:** Faça perguntas específicas para obter melhores respostas!")

def exibir_como_usar():
    st.header("ℹ️ Como usar o sistema:")
    st.write("1. Certifique-se que o banco foi criado")
    st.write("2. Digite sua pergunta")
    st.write("3. Clique em 'Buscar Resposta'")
    st.write("4. Aguarde a resposta da IA")
    
    st.markdown("---")
    st.subheader("📊 Status do Sistema:")
    if os.path.exists(DB_PATH):
        st.success("✅ Banco de dados encontrado!")
    else:
        st.error("❌ Execute o processo de criação do DB primeiro!")

def exibir_criar_db():
    st.header("🗄️ Criar Banco Vetorial")
    st.write("Crie seu banco de dados vetorial usando o script criar_db.py!")
    
    # Verificar API Key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("⚠️ API Key da OpenAI não encontrada!")
        st.write("Configure sua API Key no arquivo .env:")
        st.code("OPENAI_API_KEY=sua_chave_aqui")
        return
    else:
        st.success("✅ API Key da OpenAI configurada!")
    
    # Verificar pasta base
    base_folder = "base"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        st.info(f"📁 Pasta '{base_folder}' criada!")
    
    # Upload de arquivos
    st.subheader("📤 Upload de Arquivos PDF")
    uploaded_files = st.file_uploader(
        "Selecione os arquivos PDF:",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"📄 {len(uploaded_files)} arquivo(s) selecionado(s):")
        for file in uploaded_files:
            st.write(f"• {file.name}")
        
        if st.button("💾 Salvar Arquivos na Pasta Base"):
            with st.spinner("Salvando arquivos..."):
                for file in uploaded_files:
                    file_path = os.path.join(base_folder, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                st.success(f"✅ {len(uploaded_files)} arquivo(s) salvos em '{base_folder}'!")
    
    # Listar arquivos existentes
    st.subheader("📁 Arquivos na Pasta Base")
    if os.path.exists(base_folder):
        arquivos = [f for f in os.listdir(base_folder) if f.lower().endswith('.pdf')]
        if arquivos:
            st.write(f"📄 {len(arquivos)} arquivo(s) PDF encontrado(s):")
            for arquivo in arquivos:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {arquivo}")
                with col2:
                    if st.button("🗑️", key=f"del_{arquivo}"):
                        os.remove(os.path.join(base_folder, arquivo))
                        st.rerun()
        else:
            st.info("Nenhum arquivo PDF encontrado na pasta base.")
    
    # Botão para criar banco
    st.subheader("🚀 Criar Banco de Dados")
    if st.button("🔨 Criar Banco Vetorial", type="primary"):
        if not os.path.exists(base_folder) or not [f for f in os.listdir(base_folder) if f.lower().endswith('.pdf')]:
            st.error("❌ Nenhum arquivo PDF encontrado! Adicione arquivos primeiro.")
            return
        
        # Executar o script criar_db.py e mostrar progresso em tempo real
        import subprocess
        import sys
        
        # Container para mostrar progresso
        progress_container = st.container()
        
        with progress_container:
            st.write("🔄 **Executando script criar_db.py...**")
            
            # Placeholder para output
            output_placeholder = st.empty()
            
            try:
                # Executar o script criar_db.py
                process = subprocess.Popen(
                    [sys.executable, "criar_db.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Capturar output em tempo real
                output_lines = []
                
                with st.spinner("Processando..."):
                    for line in iter(process.stdout.readline, ''):
                        if line:
                            output_lines.append(line.strip())
                            # Mostrar as últimas 10 linhas
                            recent_output = "\n".join(output_lines[-10:])
                            output_placeholder.code(recent_output)
                    
                    process.wait()
                
                # Verificar resultado
                if process.returncode == 0:
                    st.success("🎉 Banco de dados criado com sucesso!")
                    st.balloons()
                    
                    # Verificar se o banco foi realmente criado
                    if os.path.exists(DB_PATH):
                        st.info("✨ Agora você pode fazer perguntas na Tela Principal!")
                    else:
                        st.warning("⚠️ Script executado, mas banco não encontrado.")
                else:
                    st.error(f"❌ Erro na execução (código: {process.returncode})")
                    
            except FileNotFoundError:
                st.error("❌ Arquivo criar_db.py não encontrado!")
                st.info("💡 Certifique-se que o arquivo criar_db.py está na mesma pasta.")
            except Exception as e:
                st.error(f"❌ Erro ao executar script: {str(e)}")
                st.write("**Possíveis soluções:**")
                st.write("• Verifique se o arquivo criar_db.py existe")
                st.write("• Verifique se todas as dependências estão instaladas")
                st.write("• Execute manualmente: python criar_db.py")



def main():
    st.set_page_config(
        page_title="Sistema de Perguntas e Respostas",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Sistema de Perguntas e Respostas")
    st.markdown("**Faça perguntas sobre seus documentos PDF!**")

    # Sidebar com navegação
    with st.sidebar:
        aba_selecionada = st.selectbox(
            "Escolha uma opção:", 
            ["Tela Principal", "Como Usar", "Criar DB"]
        )
        
        # Mostrar status do banco
        st.markdown("---")
        st.subheader("📊 Status")
        if os.path.exists(DB_PATH):
            st.success("✅ Banco criado")
        else:
            st.error("❌ Banco não encontrado")
    
    # Exibir conteúdo baseado na seleção
    if aba_selecionada == "Tela Principal":
        exibir_tela_principal()
    elif aba_selecionada == "Como Usar":
        exibir_como_usar()
    elif aba_selecionada == "Criar DB":
        exibir_criar_db()

# Executar a aplicação
if __name__ == "__main__":
    main()