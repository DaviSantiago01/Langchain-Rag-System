# Sistema RAG com LangChain

Sistema de perguntas e respostas sobre documentos PDF usando inteligência artificial.

## Início Rápido

1. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure sua API Key da OpenAI**
   ```bash
   # Crie um arquivo .env na raiz do projeto
   OPENAI_API_KEY=sua_chave_aqui
   ```

3. **Adicione seus PDFs**
   - Coloque os arquivos PDF na pasta `base/`

4. **Crie o banco de dados**
   ```bash
   python criar_db.py
   ```

5. **Execute a aplicação**
   ```bash
   streamlit run app_streamlit.py
   ```

## Documentação

- [📋 Funcionalidades](docs/funcionalidades.md) - Recursos e capacidades do sistema
- [🏗️ Arquitetura](docs/arquitetura.md) - Detalhes técnicos e estrutura do código

## Tecnologias

- **LangChain** - Framework para aplicações com LLM
- **OpenAI GPT-4o-mini** - Modelo de linguagem
- **ChromaDB** - Banco de dados vetorial
- **Streamlit** - Interface web
