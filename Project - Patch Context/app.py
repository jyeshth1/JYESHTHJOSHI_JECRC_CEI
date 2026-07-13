import streamlit as st
import time
from rag_pipeline import RAGPipeline

st.set_page_config(page_title="PatchContext", page_icon="🔍", layout="wide")

@st.cache_resource
def load_pipeline():
    try:
        return RAGPipeline()
    except Exception as e:
        st.error(f"Error loading RAG pipeline. Did you run the indexer? Error: {e}")
        return None

st.title("PatchContext 🔍")
st.markdown("### RAG Pipeline over the FastAPI Repository")
st.markdown("Ask questions like: *Why did FastAPI choose Pydantic v2 over v1?*")

pipeline = load_pipeline()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about FastAPI's design..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if pipeline is not None:
        with st.chat_message("assistant"):
            with st.spinner("Searching repository history and generating answer..."):
                try:
                    result = pipeline.query(prompt)
                    answer = result["answer"]
                    docs = result["docs"]
                    blocked = result.get("hallucination_blocked", False)
                    
                    st.markdown(answer)
                    
                    if blocked:
                        st.warning("⚠️ The generated answer was blocked by the NLI hallucination guard because it wasn't fully entailed by the context.")
                        with st.expander("Original Blocked Answer"):
                            st.write(result.get("original_answer", ""))
                    
                    if docs:
                        st.markdown("### Citations")
                        for i, doc in enumerate(docs):
                            doc_type = doc.metadata.get('type', 'doc').upper()
                            doc_id = doc.metadata.get('id', 'N/A')
                            url = doc.metadata.get('url', '#')
                            st.markdown(f"**[{i+1}]** [{doc_type} #{doc_id}]({url})")
                            
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"An error occurred: {e}")
