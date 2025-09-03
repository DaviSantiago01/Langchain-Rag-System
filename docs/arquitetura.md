# 🔧 Como o Sistema Funciona

## 🎯 Visão Simples
O sistema tem 3 partes principais que trabalham juntas:
1. **Interface** - onde você digita as perguntas
2. **Banco de dados** - onde ficam guardados os documentos
3. **IA** - que gera as respostas

## 📁 Arquivos Principais

### `app_streamlit.py` - A Interface
- Cria a página web que você vê
- Recebe suas perguntas
- Mostra as respostas
- Conecta com o banco de dados

### `criar_db.py` - Preparação dos Documentos
- Lê todos os PDFs da pasta `base/`
- Quebra o texto em pedaços menores
- Transforma em "linguagem de computador" (embeddings)
- Salva tudo no banco ChromaDB

### `main.py` - Funções de Apoio
- Conecta com o banco de dados
- Busca documentos relevantes
- Envia para a IA gerar resposta

## 🔄 Como Funciona na Prática

### Quando você cria o banco (só uma vez):
1. Sistema pega todos os PDFs
2. Lê o texto de cada página
3. Divide em pedaços de 1000 caracteres
4. Transforma cada pedaço em números (embeddings)
5. Salva na pasta `chroma_db/`

### Quando você faz uma pergunta:
1. Sistema transforma sua pergunta em números
2. Compara com os números dos documentos
3. Encontra os 3 pedaços mais parecidos
4. Envia tudo para o GPT-4o-mini
5. IA lê e gera uma resposta
6. Resposta aparece na tela

## 🛠️ Tecnologias Usadas

| O que faz | Tecnologia | Para que serve |
|-----------|------------|----------------|
| Interface web | Streamlit | Criar a página que você usa |
| Ler PDFs | PyPDF | Extrair texto dos arquivos |
| Banco de dados | ChromaDB | Guardar os documentos |
| IA | OpenAI GPT-4o-mini | Gerar as respostas |
| Organizar tudo | LangChain | Conectar todas as partes |

## 📂 Estrutura dos Arquivos

```
Seu Projeto/
├── app_streamlit.py      # Interface principal
├── criar_db.py           # Cria o banco de dados
├── main.py               # Funções auxiliares
├── requirements.txt      # Lista de programas necessários
├── .env                  # Sua chave da OpenAI (secreto)
├── base/                 # Coloque seus PDFs aqui
│   └── seus_pdfs.pdf
├── chroma_db/            # Banco criado automaticamente
└── docs/                 # Documentação
    ├── funcionalidades.md
    ├── arquitetura.md
    └── exemplos.md
```

## ⚙️ Configurações Importantes

- **Tamanho dos pedaços**: 1000 caracteres (para não sobrecarregar a IA)
- **Sobreposição**: 200 caracteres (para não perder contexto)
- **Documentos por resposta**: Máximo 3 (os mais relevantes)
- **Tempo limite**: 30 segundos (para não travar)

## 🔒 Segurança
- Sua chave da OpenAI fica no arquivo `.env` (não é compartilhada)
- Sistema só responde sobre seus documentos
- Não salva suas perguntas em lugar nenhum

## ⚠️ Limitações Técnicas
- Funciona melhor com poucos usuários ao mesmo tempo
- Banco de dados fica no seu computador (não na nuvem)
- Precisa recriar o banco se mudar os PDFs
- Respostas limitadas a 1000 palavras

## 💡 Possíveis Melhorias Futuras
- Suporte a Word e outros formatos
- Upload de arquivos pela interface
- Histórico de perguntas
- Versão online (na nuvem)