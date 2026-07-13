import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_vectorstore():
    if os.getenv("MOCK_MODE", "True").lower() == "true":
        from langchain_core.embeddings import FakeEmbeddings
        embeddings = FakeEmbeddings(size=1536)
    else:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        
    if not os.path.exists("faiss_index"):
        raise FileNotFoundError("FAISS index not found. Please run indexer.py first.")
    return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

class RAGPipeline:
    def __init__(self):
        self.vectorstore = get_vectorstore()
        # Use MMR to get diverse results
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 5, 'fetch_k': 20}
        )
        
        if os.getenv("MOCK_MODE", "True").lower() == "true":
            from langchain_core.runnables import RunnableLambda
            self.llm = RunnableLambda(lambda x: "This is a mock answer! Your OpenAI API key exceeded its quota, so I am running in Mock Mode. To see real generated text, please provide a working key in the .env file. The citations below, however, are retrieved from the real FastAPI data!")
        else:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert software engineer assistant for the FastAPI repository. "
                       "Answer the user's question based ONLY on the following context retrieved from the repository's "
                       "issues, pull requests, and commit history. If you don't know the answer based on the context, "
                       "say so. Always cite your sources by referencing the ID or URL of the provided context.\n\n"
                       "Context:\n{context}"),
            ("human", "{question}")
        ])
        
        # NLI-based Hallucination Guard Prompt
        self.nli_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Natural Language Inference (NLI) model. Your task is to verify if a generated response "
                       "is entailed by the provided context. If the response contains information NOT found in the context "
                       "or contradicts it, you must classify it as a hallucination.\n\n"
                       "Context:\n{context}\n\n"
                       "Generated Response:\n{response}\n\n"
                       "Respond strictly with 'YES' if the response is fully grounded in the context, and 'NO' if there is any hallucination."),
            ("human", "Is the response fully grounded in the context?")
        ])

    def format_docs(self, docs):
        formatted = []
        for d in docs:
            formatted.append(f"[{d.metadata['type'].upper()} {d.metadata['id']}] ({d.metadata['url']}):\n{d.page_content}")
        return "\n\n".join(formatted)

    def query(self, question: str):
        # 1. Retrieve
        docs = self.retriever.invoke(question)
        context_str = self.format_docs(docs)
        
        # 2. Generate
        qa_chain = self.qa_prompt | self.llm | StrOutputParser()
        answer = qa_chain.invoke({"context": context_str, "question": question})
        
        # 3. Hallucination Guard (NLI)
        if os.getenv("MOCK_MODE", "True").lower() == "true":
            entailment_result = "YES"
        else:
            nli_chain = self.nli_prompt | self.llm | StrOutputParser()
            entailment_result = nli_chain.invoke({"context": context_str, "response": answer}).strip().upper()
        
        if "YES" not in entailment_result:
            return {
                "answer": "The generated answer could not be confidently verified against the retrieved context (Hallucination blocked).",
                "docs": docs,
                "hallucination_blocked": True,
                "original_answer": answer
            }
            
        return {
            "answer": answer,
            "docs": docs,
            "hallucination_blocked": False
        }
