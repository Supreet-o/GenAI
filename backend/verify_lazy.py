import sys
import os

# Add backend to sys.path
sys.path.append(os.getcwd())

def verify_lazy_loading():
    print("Importing modules...")
    from app.core import embeddings
    from app.core import reranker
    
    print("Checking if models are loaded immediately...")
    
    if embeddings._model_instance is not None:
        print("FAIL: SentenceTransformer loaded immediately!")
    else:
        print("PASS: SentenceTransformer not loaded yet.")
        
    if reranker._reranker_instance is not None:
        print("FAIL: Reranker loaded immediately!")
    else:
        print("PASS: Reranker not loaded yet.")
        
    print("Triggering load...")
    embeddings.get_model()
    reranker.get_reranker()
    
    if embeddings._model_instance is not None:
        print("PASS: SentenceTransformer loaded on demand.")
    else:
        print("FAIL: SentenceTransformer failed to load.")
        
    if reranker._reranker_instance is not None:
        print("PASS: Reranker loaded on demand.")
    else:
        print("FAIL: Reranker failed to load.")

if __name__ == "__main__":
    try:
        verify_lazy_loading()
    except Exception as e:
        print(f"Error: {e}")
