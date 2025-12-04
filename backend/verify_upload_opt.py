import sys
import os
import asyncio
import tempfile

# Add backend to sys.path
sys.path.append(os.getcwd())

async def verify_optimization():
    print("Importing modules...")
    try:
        from app.core.parser import extract_text_from_file
        from app.api.upload import process_file
        import fitz
        import aiofiles
        print("Modules imported successfully.")
    except ImportError as e:
        print(f"Import Error: {e}")
        return

    # Create a dummy text file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as tmp:
        tmp.write("This is a test document for background processing.")
        temp_path = tmp.name
    
    print(f"Created temp file: {temp_path}")

    try:
        # Test extraction directly
        print("Testing extract_text_from_file...")
        text = await extract_text_from_file(temp_path)
        print(f"Extraction result: {text.strip()}")
        
        if text.strip() == "This is a test document for background processing.":
            print("PASS: Extraction worked.")
        else:
            print("FAIL: Extraction content mismatch.")

        # Test process_file (simulating background task)
        # Note: This will try to embed, which might fail if DB/Model isn't ready, but we catch exceptions
        print("Testing process_file...")
        await process_file(temp_path, "test_doc.txt")
        print("process_file executed (check logs for specific embedding success/fail).")

    except Exception as e:
        print(f"Error during verification: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("Cleaned up temp file.")

if __name__ == "__main__":
    asyncio.run(verify_optimization())
