import sys
import os
import numpy as np

# Add backend to sys.path
sys.path.append(os.getcwd())

from app.core.embeddings import maximal_marginal_relevance

def test_mmr():
    print("Testing MMR...")
    
    # Case 1: Standard inputs
    query = np.random.rand(384)
    embeddings = [np.random.rand(384) for _ in range(10)]
    
    try:
        indices = maximal_marginal_relevance(query, embeddings)
        print(f"Case 1 (Standard): Success. Indices: {indices}")
    except Exception as e:
        print(f"Case 1 (Standard): Failed. {e}")
        
    # Case 2: NumPy array input for embeddings
    embeddings_np = np.array(embeddings)
    try:
        indices = maximal_marginal_relevance(query, embeddings_np)
        print(f"Case 2 (NumPy): Success. Indices: {indices}")
    except Exception as e:
        print(f"Case 2 (NumPy): Failed. {e}")

    # Case 3: Single embedding
    embeddings_single = [np.random.rand(384)]
    try:
        indices = maximal_marginal_relevance(query, embeddings_single, k=1)
        print(f"Case 3 (Single): Success. Indices: {indices}")
    except Exception as e:
        print(f"Case 3 (Single): Failed. {e}")

if __name__ == "__main__":
    test_mmr()
