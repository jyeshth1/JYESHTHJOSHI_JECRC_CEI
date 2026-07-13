import streamlit as st
from src.llm import answer_question

st.set_page_config(
    page_title="CodeInsightAI",
    page_icon="💻",
    layout="wide"
)

st.title("💻 CodeInsightAI")
st.write("Ask questions about the FastAPI repository.")

question = st.text_input(
    "Ask a question",
    placeholder="Example: Why was dependency injection introduced?"
)

if st.button("Ask"):

    if question.strip():

        with st.spinner("Searching repository..."):

            answer, docs = answer_question(question)

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Sources")

        for doc in docs:

            metadata = doc.metadata

            if metadata["type"] == "commit":
                st.markdown(f"**Commit:** `{metadata['sha'][:8]}`")

            elif metadata["type"] == "pr":
                st.markdown(f"**Pull Request:** #{metadata['number']}")

            elif metadata["type"] == "issue":
                st.markdown(f"**Issue:** #{metadata['number']}")