# Sistema RAG com LangChain

Sistema de perguntas e respostas sobre documentos PDF usando inteligência artificial.

## Início Rápido

1. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure sua API Key da OpenAI**
   
   **Opção 1: Arquivo de configuração (Recomendado)**
   ```bash
   # Copie o arquivo de exemplo
   cp config_usuario.json.example config_usuario.json
   
   # Edite o arquivo e adicione sua API key
   # IMPORTANTE: Este arquivo está no .gitignore por segurança
   ```
   
   **Opção 2: Variável de ambiente**
   ```bash
   # Crie um arquivo .env na raiz do projeto
   OPENAI_API_KEY=sua_chave_aqui
   ```

3. **Adicione seus PDFs**
   - Coloque os arquivos PDF na pasta `base/`

4. **Execute a aplicação**
   ```bash
   streamlit run app_streamlit.py
   ```
   
   O banco de dados será criado automaticamente na primeira execução.

## Documentação

- [📋 Funcionalidades](docs/funcionalidades.md) - Recursos e capacidades do sistema
- [🏗️ Arquitetura](docs/arquitetura.md) - Detalhes técnicos e estrutura do código

## Tecnologias

- **LangChain** - Framework para aplicações com LLM
- **OpenAI GPT-4o-mini** - Modelo de linguagem
- **ChromaDB** - Banco de dados vetorial
- **Streamlit** - Interface web
