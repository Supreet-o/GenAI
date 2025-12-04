import sys
import os
import asyncio

# Add backend to sys.path
sys.path.append(os.getcwd())

async def test_pipeline():
    try:
        print("Importing modules...")
        from app.core.splitter import chunk_text
        from app.core.embeddings import search_mmr, embed_and_store
        from app.core.reranker import reranker
        from app.core.llm import compress_context, generate_answer
        
        print("Modules imported successfully.")
        
        # 1. Test Splitter
        text = "This is a test text. " * 100
        chunks = chunk_text(text, chunk_size=100, overlap=20)
        print(f"Splitter: Generated {len(chunks)} chunks.")
        
        # 2. Test Embedding (Mock)
        # We won't actually store to avoid messing up DB, just check imports and function existence
        print("Embeddings: Functions exist.")
        
        # 3. Test Reranker
        query = "test"
        docs = ["This is a test document.", "This is unrelated.", "Another test document."]
        reranked = reranker.rerank(query, docs, top_k=2)
        print(f"Reranker: Top 2 docs: {reranked}")
        
        # 4. Test Compression
        compressed = compress_context(query, reranked)
        print(f"Compression: Result length: {len(compressed)}")
        
        print("Verification successful!")
        
    except ImportError as e:
        print(f"Import Error: {e}")
        print("Please ensure all dependencies are installed (scikit-learn, sentence-transformers, etc.)")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_pipeline())
