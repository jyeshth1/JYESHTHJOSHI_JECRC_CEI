import os
import json
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def main():
    print("Loading data...")
    if not os.path.exists("fastapi_data.json"):
        print("Data file not found. Please run data_fetcher.py first.")
        return
        
    with open("fastapi_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    documents = []
    for item in data:
        # Create a document for each item
        content = item.get("content", "")
        if not content:
            continue
            
        doc = Document(
            page_content=content,
            metadata={
                "id": item["id"],
                "type": item["type"],
                "url": item["url"],
                "author": item.get("author", "Unknown"),
                "date": item.get("date", "Unknown"),
            }
        )
        documents.append(doc)
        
    print(f"Loaded {len(documents)} documents. Splitting text...")
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    
    print("Embedding and building FAISS index (this may take a minute)...")
    if os.getenv("MOCK_MODE", "True").lower() == "true":
        from langchain_core.embeddings import FakeEmbeddings
        embeddings = FakeEmbeddings(size=1536)
    else:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    print("Vector database saved to 'faiss_index' folder.")

if __name__ == "__main__":
    main()
