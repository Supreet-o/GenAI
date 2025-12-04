# core/llm.py
import os

try:
    import ollama
except Exception as e:
    ollama = None
    print("[WARN] ollama package not available. Install via `pip install ollama`")

LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:1b")# set in .env, e.g. llama3, llama2, mistral

def _check_ollama():
    if ollama is None:
        raise RuntimeError("Ollama not installed. Run: pip install ollama")

def generate_answer(prompt: str, max_tokens: int = 256):
    """
    Generate deterministic answer using Ollama chat.
    The prompt should instruct the model to reply only from context.
    """
    _check_ollama()
    try:
        resp = ollama.chat(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}])
        # response structure: {'message': {'content': '...'}, ...}
        return resp.get("message", {}).get("content", "").strip()
    except Exception as e:
        return f"(LLM error) {e}"

def compress_context(query: str, documents: list[str], truncate_chars: int = 4000):
    """
    Use the model to extract relevant sentences from documents.
    We do a safe truncation before calling Ollama to keep latency reasonable.
    """
    _check_ollama()
    combined = "\n\n".join(documents)
    if len(combined) > truncate_chars:
        combined = combined[:truncate_chars]

    prompt = (
        "You are a helpful assistant. Your task is to identify and extract sentences from the provided TEXT that are relevant to the QUERY.\n"
        "Return ONLY the exact sentences from the text. Do not paraphrase. Do not add conversational filler.\n"
        "If no sentences are relevant, return an empty string.\n\n"
        f"QUERY: {query}\n\n"
        f"TEXT:\n{combined}\n\n"
        "RELEVANT SENTENCES:"
    )

    try:
        resp = ollama.chat(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}])
        content = resp.get("message", {}).get("content", "").strip()
        
        # Heuristic check for refusal or failure
        lower_content = content.lower()
        if (len(content) < 5 or 
            "i cannot" in lower_content or 
            "i can't" in lower_content or 
            "sorry" in lower_content or 
            "conversation" in lower_content):
            # Fallback to original text if compression fails/refuses
            return combined[:2000]
            
        return content
    except Exception:
        # fallback: return short concatenation
        return combined[:2000]
