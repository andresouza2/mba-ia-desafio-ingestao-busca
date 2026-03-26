import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import chain
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

project_root = Path(__file__).resolve().parent.parent

@chain
def search_prompt_chain(question: dict) -> dict:
  question_chain = question["pergunta"]
  context_chain  = question["contexto"]
  return {"pergunta":question_chain, "contexto":context_chain}

def search_prompt(question=None):
  """Busca trechos semelhantes no índice PGVector com base na pergunta. Retorna contexto para responder ao usuário."""
  prompt = """
    CONTEXTO:
    {contexto}

    REGRAS:
    - Responda somente com base no CONTEXTO.
    - Se a informação não estiver explicitamente no CONTEXTO, responda:
      "Não tenho informações necessárias para responder sua pergunta."
    - Nunca invente ou use conhecimento externo.
    - Nunca produza opiniões ou interpretações além do que está escrito.

    EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
    Pergunta: "Qual é a capital da França?"
    Resposta: "Não tenho informações necessárias para responder sua pergunta."

    Pergunta: "Quantos clientes temos em 2024?"
    Resposta: "Não tenho informações necessárias para responder sua pergunta."

    Pergunta: "Você acha isso bom ou ruim?"
    Resposta: "Não tenho informações necessárias para responder sua pergunta."

    PERGUNTA DO USUÁRIO:
    {pergunta}

    RESPONDA A "PERGUNTA DO USUÁRIO"
    """

  for k in ("OPENAI_API_KEY", "PGVECTOR_URL"):
      if not os.getenv(k):
          raise RuntimeError(f"A variável de ambiente {k} não está definida")

  if not (_pgvector_collection := os.getenv("PGVECTOR_COLLECTION") or os.getenv("PGVETCOR_COLLECTION")):
      raise RuntimeError(
          "Defina PGVECTOR_COLLECTION no .env (PGVETCOR_COLLECTION também é aceito por compatibilidade)"
      )
    
  query = "Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4"

  embeddings = OpenAIEmbeddings(
    model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))

  store = PGVector(
    embeddings=embeddings,
    collection_name=_pgvector_collection,
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True,
  )

  results = store.similarity_search_with_score(query, k=10)

  parts = []
  for i, (doc, score) in enumerate(results, start=1):
    body = doc.page_content.strip()
    meta = " ".join(f"{mk}={mv}" for mk, mv in doc.metadata.items())
    parts.append(f"[trecho {i} score={score:.2f} {meta}]\n{body}")

  contexto = "\n\n---\n\n".join(parts)

  question_template = PromptTemplate(
    input_variables=["contexto", "pergunta"],
    template=prompt,
  )

  model = ChatOpenAI(
    model=os.getenv("OPENAI_CHAT_MODEL", "gpt-5-mini"),
    temperature=0,
  )
  rag_chain = search_prompt_chain | question_template | model | StrOutputParser()

  if not question:
    return None

  return rag_chain.invoke({"pergunta": question, "contexto":contexto})
