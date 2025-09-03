# 💡 Exemplos Práticos e Funções Complexas

## 🎯 O que você vai aprender aqui
Este documento explica as partes mais complicadas do sistema com exemplos práticos e linguagem simples.

## 🧩 Funções Principais Explicadas

### 1. Como o Sistema "Entende" os Documentos

**O que acontece**: O sistema transforma texto em números (embeddings)

**Exemplo prático**:
```
Texto original: "O gato subiu no telhado"
Embedding: [0.2, -0.1, 0.8, 0.3, ...] (lista com 1536 números)
```

**Por que isso é útil**:
- Textos parecidos geram números parecidos
- O computador consegue "comparar" textos usando matemática
- Funciona mesmo se você usar palavras diferentes

**Exemplo real**:
- Pergunta: "Como fazer café?"
- Documento: "Preparação de bebida com grãos torrados"
- Sistema entende que são relacionados mesmo sem palavras iguais

### 2. Como Funciona a Busca Inteligente

**Função**: `buscar_documentos_relevantes()`

**O que faz passo a passo**:
1. Pega sua pergunta: "Qual o preço do produto X?"
2. Transforma em números: [0.1, 0.5, -0.2, ...]
3. Compara com todos os documentos salvos
4. Encontra os 3 mais parecidos
5. Verifica se são "parecidos o suficiente" (score > 0.5)

**Exemplo visual**:
```
Sua pergunta: "Preço do produto X"

Documentos encontrados:
📄 Doc 1: "Produto X custa R$ 100" (Score: 0.9) ✅
📄 Doc 2: "Valores de produtos" (Score: 0.7) ✅
📄 Doc 3: "Lista de preços" (Score: 0.6) ✅
📄 Doc 4: "Como usar produto Y" (Score: 0.3) ❌ (muito baixo)
```

### 3. Como a IA Gera as Respostas

**Função**: `gerar_resposta()`

**O que acontece**:
1. Sistema pega os documentos relevantes
2. Cria um "prompt" (instrução) para a IA
3. Envia tudo para o GPT-4o-mini
4. IA lê e escreve uma resposta

**Exemplo do prompt enviado para a IA**:
```
Você é um assistente especializado em responder perguntas baseado em documentos.

Contexto dos documentos:
- Produto X custa R$ 100 e está disponível em estoque
- Valores de produtos variam conforme a categoria
- Lista de preços atualizada em janeiro de 2024

Pergunta: Qual o preço do produto X?

Instruções:
- Responda apenas com base no contexto fornecido
- Se não souber a resposta, diga que não encontrou a informação
- Seja claro e objetivo

Resposta:
```

**Resposta da IA**:
"Com base nos documentos, o produto X custa R$ 100 e está disponível em estoque."

## 🔧 Configurações Técnicas Explicadas

### Tamanho dos "Pedaços" (Chunks)

**Configuração**: 1000 caracteres por pedaço

**Por que 1000?**
- Muito pequeno: perde contexto
- Muito grande: confunde a IA
- 1000 é o equilíbrio ideal

**Exemplo prático**:
```
Documento original (3000 caracteres):
"Este manual explica como usar o produto...[texto longo]..."

Dividido em 3 pedaços:
Pedaço 1: "Este manual explica como usar o produto... (1000 chars)"
Pedaço 2: "...continuação do manual sobre instalação... (1000 chars)"
Pedaço 3: "...final do manual com troubleshooting... (1000 chars)"
```

### Sobreposição de 200 Caracteres

**O que é**: Os pedaços se "repetem" um pouco

**Por que fazer isso**:
- Evita cortar frases no meio
- Mantém o contexto entre pedaços
- Melhora a qualidade das respostas

**Exemplo visual**:
```
Pedaço 1: "...produto funciona muito bem quando usado corretamente..."
Pedaço 2: "...quando usado corretamente, é importante seguir as instruções..."
          ↑ Esta parte se repete (sobreposição)
```

## 🎮 Exemplos de Uso Real

### Exemplo 1: Manual Técnico

**Seus PDFs**: Manual de uma impressora (50 páginas)

**Pergunta**: "Como trocar o cartucho?"

**O que acontece**:
1. Sistema busca por "cartucho", "trocar", "substituir"
2. Encontra páginas 23, 24 e 25 do manual
3. IA lê essas páginas e responde:

**Resposta**: "Para trocar o cartucho: 1) Desligue a impressora, 2) Abra a tampa frontal, 3) Retire o cartucho vazio puxando a alavanca azul, 4) Insira o novo cartucho até ouvir um clique."

### Exemplo 2: Contratos

**Seus PDFs**: Contrato de trabalho (20 páginas)

**Pergunta**: "Quantos dias de férias eu tenho?"

**O que acontece**:
1. Sistema busca por "férias", "dias", "descanso"
2. Encontra cláusula específica sobre férias
3. IA responde com base no contrato

**Resposta**: "Segundo o contrato, você tem direito a 30 dias de férias por ano, que podem ser divididos em até 3 períodos."

### Exemplo 3: Artigos Acadêmicos

**Seus PDFs**: 10 artigos sobre inteligência artificial

**Pergunta**: "O que é machine learning?"

**O que acontece**:
1. Sistema busca em todos os 10 artigos
2. Encontra definições em 3 artigos diferentes
3. IA combina as informações e responde

**Resposta**: "Machine learning é uma área da inteligência artificial onde computadores aprendem padrões a partir de dados, sem serem explicitamente programados para cada tarefa específica."

## ⚠️ Quando o Sistema Não Funciona Bem

### Problema 1: PDF com Imagens
**Situação**: PDF que é só imagem (escaneado)
**O que acontece**: Sistema não consegue ler o texto
**Solução**: Use PDFs com texto selecionável

### Problema 2: Pergunta Muito Vaga
**Pergunta ruim**: "Me fale sobre isso"
**Pergunta boa**: "Qual o prazo de entrega do produto X?"
**Por que**: IA precisa de contexto específico

### Problema 3: Informação Não Existe
**Pergunta**: "Qual a cor do produto Z?"
**Se não tiver nos PDFs**: "Não encontrei informações sobre a cor do produto Z nos documentos fornecidos."
**Isso é normal**: Sistema só responde sobre o que está nos seus documentos

## 🚀 Dicas para Melhores Resultados

### 1. Organize seus PDFs
- Coloque apenas documentos relacionados na pasta `base/`
- Remova PDFs desnecessários
- Use nomes descritivos para os arquivos

### 2. Faça perguntas específicas
✅ **Bom**: "Como instalar o software na versão Windows 10?"
❌ **Ruim**: "Como instalar?"

### 3. Use palavras-chave dos documentos
- Se o documento fala "instalação", use "instalar" na pergunta
- Se fala "configuração", use "configurar"

### 4. Teste diferentes formas de perguntar
- "Qual o preço?"
- "Quanto custa?"
- "Valor do produto?"

Todas podem dar resultados ligeiramente diferentes!

## 🔍 Entendendo os Resultados

### Score de Similaridade
- **0.9-1.0**: Muito relevante (excelente match)
- **0.7-0.8**: Relevante (bom match)
- **0.5-0.6**: Pouco relevante (match fraco)
- **Abaixo de 0.5**: Irrelevante (descartado)

### Qualidade das Respostas
- **Resposta direta**: Sistema encontrou informação exata
- **Resposta parcial**: Sistema encontrou informação relacionada
- **"Não encontrei"**: Informação não existe nos documentos

Todas são respostas válidas e úteis!