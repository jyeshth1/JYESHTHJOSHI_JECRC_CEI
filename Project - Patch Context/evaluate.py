import json
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_precision,
    context_recall
)
from rag_pipeline import RAGPipeline
from dotenv import load_dotenv

load_dotenv()

# We will use a smaller subset of 5 questions for a quick evaluation demo,
# though the pipeline can evaluate 50 if provided.
BENCHMARK_QUESTIONS = [
    {"question": "Why did FastAPI migrate to Pydantic v2?", "ground_truth": "FastAPI migrated to Pydantic v2 for significant performance improvements and better typing support."},
    {"question": "What is the purpose of APIRouter?", "ground_truth": "APIRouter allows you to structure your FastAPI application by splitting path operations into multiple files/modules."},
    {"question": "How does FastAPI handle dependency injection?", "ground_truth": "FastAPI uses the `Depends` class to declare dependencies, allowing you to share logic, database connections, and enforce security policies across endpoints."},
    {"question": "Why does FastAPI use Starlette underneath?", "ground_truth": "FastAPI is built on top of Starlette to provide high performance async web capabilities, such as WebSockets and routing."},
    {"question": "What is the benefit of OpenAPI support in FastAPI?", "ground_truth": "It allows automatic generation of interactive API documentation like Swagger UI and ReDoc."}
]

def run_evaluation():
    print("Loading RAG Pipeline...")
    pipeline = RAGPipeline()
    
    questions = []
    answers = []
    contexts_list = []
    ground_truths = []
    
    print(f"Running evaluation on {len(BENCHMARK_QUESTIONS)} questions...")
    for item in BENCHMARK_QUESTIONS:
        q = item["question"]
        print(f"Evaluating: {q}")
        
        result = pipeline.query(q)
        ans = result["answer"]
        docs = result["docs"]
        
        # Ragas requires context as list of strings
        ctx = [d.page_content for d in docs]
        
        questions.append(q)
        answers.append(ans)
        contexts_list.append(ctx)
        ground_truths.append(item["ground_truth"])
        
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts_list,
        "ground_truth": ground_truths
    }
    
    dataset = Dataset.from_dict(data)
    
    print("\nRunning Ragas metrics...")
    result = evaluate(
        dataset = dataset,
        metrics=[
            answer_relevancy,
            faithfulness,
            context_precision,
            context_recall
        ],
    )
    
    df = result.to_pandas()
    print("\nEvaluation Results:")
    print(df.to_string())
    df.to_csv("evaluation_results.csv", index=False)
    print("Saved results to evaluation_results.csv")

if __name__ == "__main__":
    run_evaluation()
