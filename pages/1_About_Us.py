import streamlit as st

st.set_page_config(page_title="About Us | ABC Project Knowledge Assistant", page_icon="ℹ️", layout="wide")
st.title("ℹ️ About Us")
st.caption("Project overview | Scope, objectives, data sources and features")

st.header("Project background and problem statement")
st.write("""As projects evolve, essential information becomes dispersed across contracts, design specifications, meeting minutes, change requests, emails and reports. Project teams spend time searching for decisions, requirements and contractual obligations, creating dependencies on individual staff and increasing the risk of missed information during audits, operational queries and handovers.""")
st.info("How might we help project teams quickly locate relevant decisions, requirements and obligations across scattered project artefacts, with traceable evidence and less manual searching?")

st.header("Project objectives")
st.markdown("""- **Improve retrieval speed:** Search indexed project documents using natural-language questions.
- **Improve traceability:** Show supporting document names, pages or slides where available, and source excerpts.
- **Support continuity:** Reduce reliance on informal knowledge held by individual team members.
- **Support evidence-based responses:** Assist with requirements, decisions, obligations and SLA questions.
- **Demonstrate a scalable pattern:** Establish an MVP that can later integrate with approved repositories and access controls.""")

st.header("Scope")
left,right=st.columns(2)
with left:
    st.subheader("Included in the current MVP")
    st.markdown("""- Manual upload of PDF, DOCX, PPTX, TXT and Markdown files
- Text extraction and source-location metadata
- Overlapping text chunking and embeddings
- ChromaDB semantic vector retrieval
- LLM-generated answers grounded in retrieved excerpts
- Display of supporting source excerpts
- Duplicate detection by file-content hash""")
with right:
    st.subheader("Not yet implemented")
    st.markdown("""- User authentication or role-based permissions
- Project or document-level access segregation
- Automated email, SharePoint or repository synchronisation
- OCR for scanned documents
- Verified citation links to original files
- Document version precedence or conflict resolution
- Enterprise audit logging and durable cloud storage""")

st.header("Data sources")
st.write("The current MVP ingests only files manually uploaded by users. The following artefact types are relevant to the wider proposed solution:")
st.dataframe([
    {"Source": "Contracts and tender documents", "Current support": "Manual file upload"},
    {"Source": "Design and architecture documents", "Current support": "Manual file upload"},
    {"Source": "Functional / technical specifications and requirements", "Current support": "Manual file upload"},
    {"Source": "Meeting minutes and decision logs", "Current support": "Manual file upload"},
    {"Source": "Project reports, presentations and change requests", "Current support": "Manual file upload"},
    {"Source": "User guides and operational documents", "Current support": "Manual file upload"},
    {"Source": "Emails and connected repositories", "Current support": "Planned; no direct connector"},
], hide_index=True, use_container_width=True)

st.header("Key features")
st.markdown("""**1. Document indexing:** Extracts text, breaks it into chunks, creates vector embeddings, and stores them with metadata.

**2. Project knowledge chat:** Retrieves relevant excerpts and generates contextual answers.

**3. Source transparency:** Displays the retrieved document filename and location (PDF page, PPTX slide, or general document label).

**4. Evidence-limited answering:** Prompts the model to say when available excerpts do not establish an answer.""")

st.header("Expected benefits and limitations")
st.write("Expected benefits include faster information discovery, better continuity during team transitions and more consistent access to documented project knowledge. These are intended outcomes; the MVP has not yet been benchmarked against manual search or evaluated for answer accuracy.")
st.warning("Prototype only. No authentication, project isolation, document-level permissions or guaranteed persistence on Streamlit Community Cloud. Use synthetic or explicitly approved non-sensitive documents only.")
