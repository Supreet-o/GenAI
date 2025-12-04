import fitz  # PyMuPDF
import docx
import chardet
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .cleaner import clean_text

# Create a thread pool for CPU-bound tasks
executor = ThreadPoolExecutor(max_workers=4)

def extract_pdf_text(filepath: str) -> str:
    """Extract text from PDF using PyMuPDF (fitz)."""
    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
        raise
    return text

def extract_docx_text(filepath: str) -> str:
    """Extract text from DOCX."""
    doc = docx.Document(filepath)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_txt_text(filepath: str) -> str:
    """Extract text from TXT with encoding detection."""
    with open(filepath, "rb") as f:
        contents = f.read()
    try:
        return contents.decode("utf-8")
    except:
        enc = chardet.detect(contents)['encoding']
        return contents.decode(enc, errors="ignore")

async def extract_text_from_file(filepath: str) -> str:
    """
    Extract text from a file path asynchronously using a thread pool.
    """
    loop = asyncio.get_event_loop()
    suffix = Path(filepath).suffix.lower()
    
    raw_text = ""
    
    if suffix == ".pdf":
        raw_text = await loop.run_in_executor(executor, extract_pdf_text, filepath)
    elif suffix == ".docx":
        raw_text = await loop.run_in_executor(executor, extract_docx_text, filepath)
    elif suffix == ".txt":
        raw_text = await loop.run_in_executor(executor, extract_txt_text, filepath)
    else:
        # Fallback for other types (treat as txt or error)
        try:
            raw_text = await loop.run_in_executor(executor, extract_txt_text, filepath)
        except Exception as e:
             raise NotImplementedError(f"Unsupported file type: {suffix}")

    return clean_text(raw_text)
