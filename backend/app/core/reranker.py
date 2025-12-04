# core/reranker.py
from sentence_transformers import CrossEncoder
import numpy as np

class Reranker:
    def __init__(self, model_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        try:
            self.model = CrossEncoder(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load CrossEncoder model: {e}")

    def rerank(self, query: str, documents: list[str], top_k: int = 5) -> list[str]:
        if not documents:
            return []
        pairs = [[query, doc] for doc in documents]
        try:
            scores = self.model.predict(pairs, show_progress_bar=False)
        except Exception as e:
            print(f"[RERANK WARNING] CrossEncoder failed: {e}")
            return documents[:top_k]
        scores = np.array(scores)
        top_indices = scores.argsort()[::-1][:top_k]
        return [documents[i] for i in top_indices]

_reranker_instance = None
def get_reranker():
    global _reranker_instance
    if _reranker_instance is None:
        _reranker_instance = Reranker()
    return _reranker_instance
