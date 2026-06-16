def get_vector_store():
    embeddings = get_embedding_model()

    return Chroma(
        collection_name="enterprise_rag_db",
        embedding_function=embeddings,
        persist_directory=Config.CHROMA_DIR
    )
