import re
import unicodedata

def clean_text(text: str) -> str:
    if not text:
        return ""

    # 1) Normalize unicode (fix weird chars)
    text = unicodedata.normalize("NFKC", text)

    # 2) Remove multiple newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # 3) Remove page numbers (common patterns)
    text = re.sub(r"\bPage\s*\d+\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

    # 4) Remove headers / footers (common across pages)
    # Example: repeated header/footer lines appear 10+ times
    lines = text.split("\n")
    freq = {}
    for line in lines:
        striped = line.strip()
        if len(striped) > 0:
            freq[striped] = freq.get(striped, 0) + 1

    repeated_headers = {k for k, v in freq.items() if v > 8}  # appears many times
    cleaned_lines = [ln for ln in lines if ln.strip() not in repeated_headers]

    text = "\n".join(cleaned_lines)

    # 5) Fix hyphenated breaks: "para-\ngraph" → "paragraph"
    text = re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)

    # 6) Merge broken lines within a paragraph
    text = re.sub(r"(?<!\.)\n(?=[a-z])", " ", text)

    # 7) Remove long sequences of symbols
    text = re.sub(r"[=]{3,}|[-]{5,}|[_]{5,}", " ", text)

    # 8) Condense extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text
