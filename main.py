# main.py - Sistema de Perguntas e Respostas baseado em documentos
from langchain_chroma import Chroma  # Banco de dados vetorial (armazena embeddings)
from langchain_openai import OpenAIEmbeddings  # Função para criar embeddings (converter texto em números)
from langchain.prompts import ChatPromptTemplate  # Template para prompts (estruturas de mensagem)
from langchain_openai import ChatOpenAI  # Modelo de linguagem da OpenAI (IA que responde)
from dotenv import load_dotenv  # Carregar variáveis de ambiente (como chaves de API)

print("Iniciando sistema de perguntas e respostas...")
load_dotenv()

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

def perguntar():
    """
    Esta função serve para:
    1. Receber uma pergunta do usuário
    2. Buscar documentos relevantes no banco de dados
    3. Filtrar por relevância e enviar para IA
    4. Retornar a resposta baseada nos documentos
    """
    
    try:
        print("\n--- Novo processo de busca iniciado ---")
        
        # 1. Coletar pergunta do usuário
        pergunta = input("Digite sua pergunta: ")

        # Verificar se a pergunta não está vazia
        if not pergunta.strip():  # .strip() remove espaços vazios do início e fim
            print("Por favor, digite uma pergunta válida.")
            return

        print(f"Pergunta recebida: {pergunta}")

        # 2. Conectar ao banco de dados vetorial
        print("Conectando ao banco de dados...")
        funcao_embedding = OpenAIEmbeddings()  # Inicializar embeddings da OpenAI (converte texto em vetores)
        
        try:  # try/except captura erros e permite tratamento
            db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)  # Carregar banco de dados (Chroma = tipo de banco vetorial)
            print("Banco de dados carregado com sucesso!")
        except Exception as e:  # Exception = qualquer tipo de erro que pode acontecer
            print(f"Erro ao carregar o banco de dados: {e}")
            print("Execute 'python criar_db.py' primeiro para criar o banco!")
            return

        # 3. Buscar documentos relevantes
        print("Buscando documentos relevantes...")
        resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)  # Busca os 3 documentos mais similares (aumentado de 2 para 3)
        print(f"Documentos encontrados: {len(resultados)}")  # len() = conta quantos itens tem na lista
        
        # Mostrar scores de relevância e prévia do conteúdo
        for i, (doc, score) in enumerate(resultados):  # enumerate() = adiciona contador automático, (doc, score) = desempacota tupla
            print(f"Documento {i+1} - Score: {score:.3f}")  # :.3f = mostra 3 casas decimais
            print(f"  Prévia: {doc.page_content[:150]}...")  # Mostra primeiros 150 caracteres

        # 4. Filtrar por relevância (threshold = 0.5)
        if len(resultados) == 0 or resultados[0][1] < 0.5:
            print("Nenhum documento relevante encontrado.")
            return
        
        print("Documentos relevantes aprovados!")

        # 5. Extrair textos dos documentos
        textos_resultado = []  # Lista vazia para armazenar textos
        for resultado in resultados:  # Para cada documento encontrado
            texto = resultado[0].page_content  # Extrair conteúdo do documento (resultado[0] = documento, [1] = score)
            textos_resultado.append(texto)  # .append() = adiciona item ao final da lista
        
        documentos = "\n\n----\n\n".join(textos_resultado)  # .join() = junta lista em string única com separador
        
        # 6. Criar prompt estruturado
        print("Criando prompt para IA...")
        prompt = ChatPromptTemplate.from_template(prompt_template)  # Cria template estruturado (from_template = a partir do modelo)
        prompt_formatado = prompt.invoke({"pergunta": pergunta, "documentos": documentos})  # .invoke() = executar/aplicar, substitui variáveis no template

        # 7. Enviar para modelo de IA
        print("Consultando IA...")
        modelo = ChatOpenAI(model="gpt-5-nano")  # Inicializa modelo específico da OpenAI (gpt-4o-mini = versão do modelo)
        resposta = modelo.invoke(prompt_formatado)  # .invoke() = chama a IA com o prompt
        
        # 8. Exibir resposta
        print("\n=== RESPOSTA ===")
        print(resposta.content)  # .content = extrai apenas o texto da resposta (sem metadados)
        print("================")

    except Exception as e:  # Captura qualquer erro não previsto
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    perguntar()
