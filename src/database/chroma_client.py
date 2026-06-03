from langchain_community.vectorstores import Chroma
from src.database.embeddings import get_embedding_model
from src.config import Config

def get_vector_store():
    embeddings = get_embedding_model()
    return Chroma(
        collection_name="enterprise_rag_db",
        embedding_function=embeddings,
        persist_directory=Config.CHROMA_DIR
    )
