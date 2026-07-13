from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from src.chunker import chunk_documents


class BGEEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def embed_documents(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )
        return embeddings.tolist()

    def embed_query(self, text):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()


def build_vectorstore():

    chunks = chunk_documents()

    embedding_model = BGEEmbeddings()

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    vectorstore.save_local("vectorstore")

    print(f"Saved {len(chunks)} chunks to FAISS.")


if __name__ == "__main__":
    build_vectorstore()