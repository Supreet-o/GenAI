# RAG WebApp — MVP Code Bundle

This archive contains a minimal MVP scaffold for a Retrieval-Augmented Generation (RAG) web app:
- backend: FastAPI app that accepts document uploads, extracts text, embeds and stores in ChromaDB, and answers queries using a local LLM pipeline.
- frontend: Minimal React (Vite) client with Upload and Chat components.
- docker-compose.yml, Dockerfiles, and run instructions.

## Run (dev)
1. Backend
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Frontend
   ```bash
   cd frontend/client
   npm install
   npm run dev -- --host
   ```

Open http://localhost:5173 for the frontend and http://localhost:8000/docs for API docs.
