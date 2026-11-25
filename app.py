import streamlit as st
from rag import COLLECTION, answer, index_file

st.set_page_config(page_title="ABC Project Knowledge Assistant", page_icon="📚", layout="wide")
st.title("📚 ABC Project Knowledge Assistant")
st.caption("Local development MVP · RAG with source citations")

with st.sidebar:
    st.header("Knowledge base")
    st.metric("Indexed text chunks", COLLECTION.count())
    uploads = st.file_uploader("Upload project documents", type=["pdf", "docx", "pptx", "txt", "md"],
                               accept_multiple_files=True)
    if st.button("Index selected documents", disabled=not uploads):
        for file in uploads or []:
            try:
                count = index_file(file.name, file.getvalue())
                st.success(f"{file.name}: {count} new chunks" if count else f"{file.name}: already indexed")
            except Exception as exc:
                st.error(f"{file.name}: {exc}")
        st.rerun()
    st.info("Prototype only: no authentication, project isolation, or document-level permissions.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Retrieved source excerpts"):
                for source in message["sources"]:
                    st.markdown(f"**[Source {source['number']}] {source['filename']} — {source['location']}**")
                    st.write(source["text"])

if question := st.chat_input("Ask about decisions, requirements, SLAs, or contracts..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching project knowledge..."):
                response, sources = answer(question)
            st.markdown(response)
            if sources:
                with st.expander("Retrieved source excerpts"):
                    for source in sources:
                        st.markdown(f"**[Source {source['number']}] {source['filename']} — {source['location']}**")
                        st.write(source["text"])
            st.session_state.messages.append({"role": "assistant", "content": response, "sources": sources})
        except Exception as exc:
            st.error(f"Unable to answer: {exc}")
