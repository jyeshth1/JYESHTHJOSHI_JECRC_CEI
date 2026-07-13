from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


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


embedding_model = BGEEmbeddings()

vectorstore = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)


retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)


if __name__ == "__main__":

    query = input("Ask a question: ")

    docs = retriever.invoke(query)

    print("\nRetrieved Documents:\n")

    for i, doc in enumerate(docs, 1):
        print(f"Document {i}")
        print(doc.page_content)
        print(doc.metadata)
        print("-" * 60)