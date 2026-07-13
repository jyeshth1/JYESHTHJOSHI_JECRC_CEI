import os
from dotenv import load_dotenv
from groq import Groq

from src.retriever import retriever

load_dotenv()

client = Groq(
    api_key=os.getenv("groq_api_key")
)


def answer_question(question):
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a helpful software engineering assistant.

Answer ONLY using the repository context provided below.

If the answer is not present in the context, reply exactly:
"I couldn't find enough information in the repository."

Repository Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content

    return answer, docs