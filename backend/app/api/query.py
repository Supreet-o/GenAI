# app/api/query.py  (or wherever your router lives)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.embeddings import search_mmr
from ..core.reranker import get_reranker
from ..core.llm import generate_answer, compress_context

router = APIRouter()

class QueryReq(BaseModel):
    query: str

@router.post("/")
async def do_query(req: QueryReq):
    try:
        q = req.query.strip()
        if not q:
            return {"answer": "Empty query provided.", "sources": []}

        # 1) Retrieve candidates using MMR (fetch many)
        results = search_mmr(q, n_results=10, fetch_k=25)
        docs = results.get("documents", [[]])[0]

        if not docs:
            return {"answer": "No relevant data found in the uploaded PDFs.", "sources": []}

        # 2) Rerank top candidates
        reranker = get_reranker()
        top_docs = reranker.rerank(q, docs, top_k=5)
        print(f"DEBUG: Top {len(top_docs)} docs after rerank: {top_docs}")

        # 3) Compress context (LLM-assisted extraction)
        compressed = compress_context(q, top_docs)
        print(f"DEBUG: Compressed context: {compressed}")
        
        # additionally slice each fragment to keep prompt bounded
        fragments = [frag.strip()[:800] for frag in compressed.split("\n") if frag.strip()]
        # if compress returns empty, fallback to top_docs (safely truncated)
        if not fragments:
            print("DEBUG: Compression returned empty, falling back to top_docs.")
            fragments = [d[:800] for d in top_docs]

        context = "\n\n".join(fragments[:5])  # join up to 5 fragments
        print(f"DEBUG: Final Context passed to LLM:\n{context}")

        # 4) Build strict instruction prompt (force model to say not found)
        prompt = (
            "You are a helpful assistant. Answer the QUESTION based on the CONTEXT below.\n"
            "If the context mentions the topic, summarize what it says.\n"
            "Only say 'Not found in the PDF' if the context is completely unrelated.\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"QUESTION:\n{q}\n\n"
            "ANSWER:"
        )

        answer = generate_answer(prompt)
        return {"answer": answer.strip(), "sources": docs[:5]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {e}")
