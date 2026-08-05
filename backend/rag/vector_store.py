from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


_vector_store = None


def get_vector_store():
    global _vector_store

    if _vector_store is None:

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        _vector_store = Chroma(
            persist_directory="backend/rag/chroma_db",
            embedding_function=embeddings
        )

    return _vector_store