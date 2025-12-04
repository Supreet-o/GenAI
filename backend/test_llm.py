import sys
import os

# Add backend to sys.path
sys.path.append(os.getcwd())

try:
    from app.core.llm import generate_answer
    print("Successfully imported generate_answer")
    
    answer = generate_answer("What is the capital of France?")
    print(f"Answer: {answer}")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
