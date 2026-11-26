import streamlit as st

st.set_page_config(page_title="Methodology | ABC Project Knowledge Assistant", page_icon="🧭", layout="wide")
st.title("🧭 Methodology")
st.caption("Architecture, data flows, implementation details and use-case flowcharts")

st.header("1. Implementation approach")
st.write("The application uses Retrieval Augmented Generation (RAG). Uploaded documents are extracted and indexed separately from the question-answering flow. During a chat, the system retrieves semantically relevant passages and supplies them to an OpenAI model as evidence.")

st.header("2. High-level architecture")
st.graphviz_chart(r"""digraph architecture {
rankdir=TB; graph [bgcolor="transparent", pad="0.2", nodesep="0.35", ranksep="0.5"];
node [shape=box, style="rounded,filled", fillcolor="#E9F1FB", color="#6388B4", fontname="Helvetica"];
"Project user" -> "Streamlit UI (app.py)";
"Streamlit UI (app.py)" -> "RAG orchestration (rag.py)";
"RAG orchestration (rag.py)" -> "Text extraction / chunking" [label="upload"];
"Text extraction / chunking" -> "OpenAI embeddings";
"OpenAI embeddings" -> "ChromaDB (chunks + metadata)";
"RAG orchestration (rag.py)" -> "ChromaDB (chunks + metadata)" [label="retrieve"];
"RAG orchestration (rag.py)" -> "OpenAI chat model" [label="question + evidence"];
"OpenAI chat model" -> "Streamlit UI (app.py)" [label="answer"];
}""", use_container_width=True)

st.header("3. Use case A — Document ingestion and indexing")
st.write("Trigger: a user uploads one or more supported documents and selects **Index selected documents**.")
st.graphviz_chart(r"""digraph ingest {
rankdir=TB; graph [bgcolor="transparent", nodesep="0.25", ranksep="0.35"];
node [shape=box, style="rounded,filled", fillcolor="#E9F1FB", color="#6388B4", fontname="Helvetica"];
start [label="Upload document"];
valid [label="Supported format?", shape=diamond, fillcolor="#FFF3DA"];
extract [label="Extract text and source location"];
nonempty [label="Extractable text?", shape=diamond, fillcolor="#FFF3DA"];
chunk [label="Split into overlapping chunks"];
duplicate [label="Already indexed?", shape=diamond, fillcolor="#FFF3DA"];
embed [label="Create OpenAI embeddings"];
store [label="Upsert vectors, chunks and metadata into ChromaDB", fillcolor="#E1F4E9"];
start -> valid; valid -> extract [label="Yes"]; valid -> invalid [label="No"];
invalid [label="Show unsupported format error", fillcolor="#FCE8E6"];
extract -> nonempty; nonempty -> empty [label="No"];
empty [label="Report no extractable text / OCR needed", fillcolor="#FCE8E6"];
nonempty -> chunk [label="Yes"]; chunk -> duplicate;
duplicate -> skip [label="Yes"]; skip [label="Skip duplicate"];
duplicate -> embed [label="No"]; embed -> store;
}""", use_container_width=True)
with st.expander("Implementation details: indexing", expanded=True):
    st.markdown("""1. `extract()` uses PyMuPDF for PDF, python-docx for DOCX, python-pptx for PPTX, and UTF-8 decoding for TXT/MD.
2. `chunks()` uses approximately **1,200 characters** with **200-character overlap**, preferring a whitespace boundary.
3. `index_file()` computes a SHA-256 digest and skips a file if its first chunk ID is already indexed.
4. `embed()` calls the configured OpenAI embedding model in batches of up to **64 chunks**.
5. `COLLECTION.upsert()` stores chunk text, vectors, filename, source location and hash in local persistent ChromaDB.
6. Scanned image-only PDFs are not OCR-processed in the MVP.""")

st.header("4. Use case B — Chat with project knowledge")
st.write("Trigger: a user asks a natural-language question in the chatbot.")
st.graphviz_chart(r"""digraph chat {
rankdir=TB; graph [bgcolor="transparent", nodesep="0.25", ranksep="0.35"];
node [shape=box, style="rounded,filled", fillcolor="#E9F1FB", color="#6388B4", fontname="Helvetica"];
ask [label="User asks question"];
ready [label="Any indexed chunks?", shape=diamond, fillcolor="#FFF3DA"];
noindex [label="Request document indexing", fillcolor="#FCE8E6"];
qembed [label="Generate question embedding"];
search [label="ChromaDB cosine vector search (up to 6 chunks)"];
context [label="Build numbered source excerpts"];
llm [label="Send question + evidence to OpenAI chat model"];
answer [label="Show answer and retrieved excerpts", fillcolor="#E1F4E9"];
ask -> ready; ready -> noindex [label="No"];
ready -> qembed [label="Yes"]; qembed -> search; search -> context;
context -> llm; llm -> answer;
}""", use_container_width=True)
with st.expander("Implementation details: question answering", expanded=True):
    st.markdown("""1. `answer()` checks whether the ChromaDB collection has any chunks.
2. It embeds the user's question using the configured OpenAI embedding model.
3. ChromaDB returns up to **6 nearest chunks** and associated filenames, locations and distances.
4. The app constructs `[Source N]`-labelled excerpts and instructs the chat model to answer only from this evidence.
5. The response and retrieved excerpts are displayed in Streamlit.
6. The app does **not** currently apply a relevance threshold, verify citations independently or retain chat history in the model request; Streamlit session state stores the visible conversation only.""")

st.header("5. Key technical components")
st.dataframe([
    {"Layer": "Interface", "Technology": "Streamlit", "Responsibility": "File upload, indexing controls, chat display"},
    {"Layer": "Orchestration", "Technology": "Python (rag.py)", "Responsibility": "Extraction, chunking, retrieval, prompt assembly"},
    {"Layer": "Embeddings", "Technology": "OpenAI API", "Responsibility": "Vectorise document chunks and questions"},
    {"Layer": "Vector store", "Technology": "ChromaDB PersistentClient", "Responsibility": "Store and search vectors and source metadata"},
    {"Layer": "Generation", "Technology": "OpenAI chat completions", "Responsibility": "Compose evidence-grounded responses"},
], hide_index=True, use_container_width=True)

st.header("6. Constraints, risks and planned improvements")
st.markdown("""- **Security:** No authentication, access filtering or project isolation; add these before using real restricted project information.
- **Storage:** ChromaDB is stored in the app filesystem; Community Cloud filesystem persistence is not guaranteed.
- **Source fidelity:** PDF pages and PowerPoint slides are labelled, but DOCX is labelled only as `document`.
- **Data quality:** Image-only scans require OCR; tables and complex layouts may be imperfectly extracted.
- **Answer assurance:** Add evaluation datasets, relevance thresholds, citation verification and document version management.
- **Repository integration:** Approved email and SharePoint connections are future enhancements, not current features.""")
st.caption("These diagrams document the actual MVP code paths rather than a proposed future-state enterprise implementation.")
