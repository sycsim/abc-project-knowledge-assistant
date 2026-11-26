ABC Project Knowledge Assistant — Streamlit multipage MVP
Pages
`app.py` — Chatbot / upload and index documents
`pages/1_About_Us.py` — Project background, scope, objectives, sources and features
`pages/2_Methodology.py` — Architecture and separate ingestion/chat flowcharts
Run locally
Use Python 3.12:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```
Create `.env` (never commit it):
```env
OPENAI_API_KEY=your_key
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```
Run `python -m streamlit run app.py`.
Streamlit Community Cloud
Push files to GitHub excluding `.env`, `.venv` and `data/`. Deploy `app.py` as entrypoint with Python 3.12. In Streamlit app settings > Secrets set the three variables above using TOML string syntax. Root-level Streamlit secrets are exposed as environment variables, compatible with the existing `rag.py`.
Important limits
This is a single-user demonstration, not a secured enterprise system. No authentication, document permissions or project isolation. Uploaded content is sent to the configured OpenAI API. Community Cloud local ChromaDB is not durable across restarts. Use synthetic or approved non-sensitive documents only.
Reference sample
The requested external sample PDF could not be fetched at preparation time. The diagrams and content are grounded in the provided application code and the project description rather than a verified reproduction of the sample slides.
