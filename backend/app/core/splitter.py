# core/splitter.py
import re

class SimpleTextSplitter:
    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str):
        # normalize whitespace, keep basic punctuation
        clean = re.sub(r'\s+', ' ', text).strip()
        chunks = []
        start = 0
        L = len(clean)
        while start < L:
            end = min(start + self.chunk_size, L)
            chunk = clean[start:end]
            chunks.append(chunk)
            start += (self.chunk_size - self.chunk_overlap)
        return chunks

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50):
    return SimpleTextSplitter(chunk_size, overlap).split_text(text)
