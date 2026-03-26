import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()
for k in ("OPENAI_API_KEY", "PGVECTOR_URL"):
    if not os.getenv(k):
        raise RuntimeError(f"A variável de ambiente {k} não está definida")

_pgvector_collection = os.getenv("PGVECTOR_COLLECTION") or os.getenv("PGVETCOR_COLLECTION")
if not _pgvector_collection:
    raise RuntimeError(
        "Defina PGVECTOR_COLLECTION no .env (PGVETCOR_COLLECTION também é aceito por compatibilidade)"
    )

project_root = Path(__file__).resolve().parent.parent
_pdf = os.getenv("PDF_PATH", "document.pdf")
pdf_path = Path(_pdf) if Path(_pdf).is_absolute() else project_root / _pdf

docs = PyPDFLoader(str(pdf_path)).load()

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=150, 
    add_start_index=False).split_documents(docs)

if not splits:
    raise SystemExit(0)

enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in splits
]

ids = [f"doc-{i}" for i in range(len(enriched))]

embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))

store = PGVector(
    embeddings=embeddings,
    collection_name=_pgvector_collection,
    connection=os.getenv("PGVECTOR_URL"),
    use_jsonb=True
)

store.add_documents(enriched, ids=ids)