from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

client = QdrantClient(
    url=Config.QDRANT_URL,
    api_key=Config.QDRANT_API_KEY,
)

vectorstore = QdrantVectorStore(
    client=client,
    collection_name="enterprise_rag_db",
    embedding=get_embedding_model()
)
