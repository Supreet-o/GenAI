# core/embeddings.py
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# init chroma
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# model singleton
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def embed_and_store(documents: list[str], filename: str = None, collection_name: str = "documents"):
    """
    Embed a list of text chunks and upsert to Chroma collection.
    Returns list of ids created.
    """
    if not documents:
        return []

    model = get_model()
    embeddings = model.encode(documents, show_progress_bar=False)
    collection = _client.get_or_create_collection(name=collection_name)

    # generate unique ids if not provided
    ids = [f"{filename}_{i}_{np.random.randint(1e6)}" for i in range(len(documents))]
    metadatas = [{"filename": filename} for _ in documents]

    # add or upsert
    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        ids=ids,
        metadatas=metadatas
    )
    return ids

def search_similar(query: str, n_results: int = 5):
    """
    Simple similarity search wrapper returning Chroma query result.
    """
    collection = _client.get_collection(name="documents")
    model = get_model()
    q_emb = model.encode([query]).tolist()
    res = collection.query(query_embeddings=q_emb, n_results=n_results, include=["documents", "metadatas"])
    return res

def maximal_marginal_relevance(query_embedding, embedding_list, lambda_mult=0.5, k=4):
    """
    MMR selection (safe shapes).
    query_embedding: 1D numpy array
    embedding_list: list of lists (or 2D numpy array)
    returns indices selected
    """
    if len(embedding_list) == 0:
        return []

    emb = np.array(embedding_list)
    # ensure shapes
    if query_embedding.ndim == 2:
        q = query_embedding[0]
    else:
        q = query_embedding

    # cosine similarity to query
    sim_to_query = cosine_similarity(q.reshape(1, -1), emb).flatten()
    # pick highest as first
    first = int(np.argmax(sim_to_query))
    selected = [first]

    # precompute similarity matrix between candidates
    sim_matrix = cosine_similarity(emb, emb)

    while len(selected) < min(k, emb.shape[0]):
        best_score = -np.inf
        best_idx = None
        for i in range(emb.shape[0]):
            if i in selected:
                continue
            relevance = sim_to_query[i]
            redundancy = max(sim_matrix[i][j] for j in selected)
            score = lambda_mult * float(relevance) - (1 - lambda_mult) * float(redundancy)
            if score > best_score:
                best_score = score
                best_idx = i
        if best_idx is None:
            break
        selected.append(best_idx)
    return selected

def search_mmr(query: str, n_results: int = 5, fetch_k: int = 20, lambda_mult: float = 0.5):
    """
    1) query chroma for top `fetch_k` candidates
    2) apply MMR on returned embeddings
    3) return documents selected
    """
    collection = _client.get_collection(name="documents")
    model = get_model()
    q_emb = model.encode([query])  # shape (1, dim)
    # fetch candidates with embeddings
    res = collection.query(query_embeddings=[q_emb.tolist()[0]], n_results=fetch_k, include=["documents", "embeddings", "metadatas"])
    if not res or len(res.get("embeddings", [])) == 0 or len(res["embeddings"][0]) == 0:
        return {"documents": [[]], "ids": [[]], "metadatas": [[]], "embeddings": [[]]}

    embeddings = res["embeddings"][0]  # list of lists
    documents = res["documents"][0]
    ids = res["ids"][0]
    metadatas = res["metadatas"][0]

    # run MMR to pick top n_results
    try:
        selected_idx = maximal_marginal_relevance(q_emb[0], embeddings, lambda_mult=lambda_mult, k=n_results)
    except Exception as e:
        # fallback to first-n
        selected_idx = list(range(min(n_results, len(documents))))

    final_docs = [documents[i] for i in selected_idx]
    final_ids = [ids[i] for i in selected_idx]
    final_metas = [metadatas[i] for i in selected_idx]

    return {
        "documents": [final_docs],
        "ids": [final_ids],
        "metadatas": [final_metas],
        "embeddings": [ [embeddings[i] for i in selected_idx] ]
    }
