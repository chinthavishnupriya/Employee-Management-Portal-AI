from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.rag.vector_store import get_vector_store
from backend.ai.llm_service import llm


class RAGService:

    def ingest_pdf(self, file_path: str):

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(documents)

        get_vector_store().add_documents(chunks)

        return len(chunks)

    def ask(self, question: str):

        docs = get_vector_store().similarity_search(
            question,
            k=4
        )

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are an HR Policy Assistant.

Answer ONLY using the policy information below.

If the answer is not available in the policy,
reply:

"I couldn't find that information in the uploaded HR policy."

HR Policy:

{context}

Question:
{question}
"""

        return llm.ask(prompt)


rag_service = RAGService()