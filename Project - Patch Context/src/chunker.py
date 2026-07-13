from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.loader import load_all_documents



def chunk_documents():
    documents = load_all_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":
    chunks = chunk_documents()

    print(f"Original Documents: {len(load_all_documents())}")
    print(f"Total Chunks: {len(chunks)}")

    print("\nFirst Chunk:\n")
    print(chunks[0])