from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from ..core.parser import extract_text_from_file
from ..core.embeddings import embed_and_store
from ..core.splitter import chunk_text
import uuid
import os
import aiofiles
import tempfile
import asyncio

router = APIRouter()

async def save_file_streaming(file: UploadFile) -> str:
    """Save upload file to temp file using streaming."""
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        temp_path = tmp.name
    
    async with aiofiles.open(temp_path, 'wb') as out_file:
        while content := await file.read(1024 * 1024):  # Read in 1MB chunks
            await out_file.write(content)
            
    return temp_path

async def process_file(file_path: str, filename: str):
    """Background task to process the file."""
    try:
        print(f"Processing file: {filename}")
        text = await extract_text_from_file(file_path)
        
        if not text or len(text.strip()) == 0:
            print(f"Warning: Empty content in {filename}")
            return

        chunks = chunk_text(text)
        ids = embed_and_store(chunks, filename=filename)
        print(f"Successfully processed {filename}: {len(ids)} chunks stored.")
        
    except Exception as e:
        print(f"Error processing {filename}: {e}")
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        file_path = await save_file_streaming(file)
        background_tasks.add_task(process_file, file_path, file.filename)
        return {"status": "File received, processing in background", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
