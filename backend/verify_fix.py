import sys
import os

# Add backend to sys.path
sys.path.append(os.getcwd())

try:
    from app.core.embeddings import embed_and_store
    print("Successfully imported embed_and_store")
    
    ids = embed_and_store(["This is a test document."], filename="test.txt")
    print(f"Successfully stored document with IDs: {ids}")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
