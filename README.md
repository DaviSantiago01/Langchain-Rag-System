# 🤖 Sistema RAG com LangChain e ChromaDB

Um sistema de **Retrieval-Augmented Generation (RAG)** que permite fazer perguntas sobre documentos PDF usando inteligência artificial. O projeto utiliza LangChain, ChromaDB e OpenAI para criar um assistente inteligente baseado em documentos.

## 🎯 Funcionalidades

- **📄 Processamento de PDFs**: Carrega e processa múltiplos documentos PDF
- **🔍 Busca Semântica**: Encontra informações relevantes usando embeddings vetoriais
- **🧠 IA Conversacional**: Responde perguntas baseadas exclusivamente no conteúdo dos documentos
- **💾 Banco Vetorial**: Armazena embeddings usando ChromaDB para buscas eficientes
- **⚡ Respostas Contextuais**: Fornece respostas precisas com base no contexto dos documentos

## 🏗️ Arquitetura

```
📁 Projeto RAG
├── 📄 main.py              # Sistema principal de perguntas e respostas
├── 📄 criar_db.py          # Criação e população do banco vetorial
├── 📁 base/                # Pasta para documentos PDF
│   └── 📄 *.pdf           # Seus documentos PDF
├── 📁 db/                  # Banco de dados ChromaDB
│   ├── 📄 chroma.sqlite3   # Banco SQLite do Chroma
│   └── 📁 collections/     # Coleções de embeddings
├── 📄 .env                 # Variáveis de ambiente
└── 📁 venv/                # Ambiente virtual Python
```

## 🚀 Como Funciona

### 1. **Preparação dos Documentos**
- Os PDFs são carregados da pasta `base/`
- Documentos são divididos em chunks de 1000 caracteres
- Cada chunk é convertido em embeddings usando OpenAI
- Embeddings são armazenados no ChromaDB

### 2. **Processo de Consulta**
- Usuário faz uma pergunta
- Sistema converte pergunta em embedding
- Busca os 3 chunks mais similares no banco
- Filtra resultados por relevância (score > 0.5)
- Envia contexto + pergunta para GPT-4
- Retorna resposta baseada apenas nos documentos

## 📋 Pré-requisitos

- Python 3.8+
- Conta OpenAI com API Key
- Documentos PDF para consulta

## ⚙️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/langchain-rag-system.git
cd langchain-rag-system
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install langchain langchain-openai langchain-chroma langchain-community
pip install chromadb pypdf python-dotenv
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave_api_aqui
```

### 5. Adicione seus documentos
- Coloque seus arquivos PDF na pasta `base/`
- Certifique-se de que os PDFs contêm texto (não apenas imagens)

## 🎮 Como Usar

### 1. **Criar o Banco de Dados**
```bash
python criar_db.py
```
Este comando irá:
- Ler todos os PDFs da pasta `base/`
- Dividir em chunks menores
- Criar embeddings
- Salvar no banco ChromaDB

### 2. **Fazer Perguntas**
```bash
python main.py
```
Digite suas perguntas e receba respostas baseadas nos documentos!

## 💡 Exemplo de Uso

```
$ python main.py
Digite sua pergunta: Quais são os principais benefícios do Python?

=== RESPOSTA ===
Baseado nos documentos fornecidos, os principais benefícios do Python são:

1. **Simplicidade**: Sintaxe clara e legível
2. **Versatilidade**: Usado em web, IA, análise de dados
3. **Comunidade**: Grande ecossistema de bibliotecas
4. **Produtividade**: Desenvolvimento rápido de aplicações
================
```

## 🔧 Configurações Avançadas

### Ajustar Tamanho dos Chunks
No arquivo `criar_db.py`, modifique:
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Tamanho do chunk
    chunk_overlap=200,    # Sobreposição
)
```

### Alterar Número de Documentos Retornados
No arquivo `main.py`, modifique:
```python
resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)  # Altere k
```

### Ajustar Filtro de Relevância
No arquivo `main.py`, modifique:
```python
if resultados[0][1] < 0.5:  # Altere o threshold
```

## 📊 Tecnologias Utilizadas

| Tecnologia | Função |
|------------|--------|
| **LangChain** | Framework para aplicações com LLM |
| **ChromaDB** | Banco de dados vetorial |
| **OpenAI GPT-4** | Modelo de linguagem |
| **OpenAI Embeddings** | Conversão texto → vetores |
| **PyPDF** | Leitura de documentos PDF |
| **Python-dotenv** | Gerenciamento de variáveis de ambiente |

## 🔍 Estrutura do Código

### `main.py` - Sistema Principal
- **`perguntar()`**: Função principal que processa consultas
- Conecta ao banco ChromaDB
- Realiza busca semântica
- Filtra por relevância
- Gera resposta contextual

### `criar_db.py` - Criação do Banco
- **`carregar_documentos()`**: Lê PDFs da pasta base
- **`dividir_documentos()`**: Divide em chunks menores
- **`vetorizar_chunks()`**: Cria embeddings e salva no banco

## 🚨 Solução de Problemas

### Erro: "Banco de dados não encontrado"
```bash
python criar_db.py  # Recrie o banco
```

### Erro: "Nenhum documento relevante encontrado"
- Verifique se os PDFs estão na pasta `base/`
- Tente reformular a pergunta
- Reduza o threshold de relevância

### Erro: "OpenAI API Key inválida"
- Verifique se a chave está correta no arquivo `.env`
- Confirme se a conta OpenAI tem créditos

## 📈 Melhorias Futuras

- [ ] Interface web com Streamlit/Gradio
- [ ] Suporte a outros formatos (DOCX, TXT)
- [ ] Cache de respostas frequentes
- [ ] Métricas de qualidade das respostas
- [ ] Suporte a múltiplos idiomas
- [ ] API REST para integração

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)

## 🙏 Agradecimentos

- [LangChain](https://langchain.com/) pela excelente framework
- [ChromaDB](https://www.trychroma.com/) pelo banco vetorial eficiente
- [OpenAI](https://openai.com/) pelos modelos de IA

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐