import re
from typing import List

WORD_RE = re.compile(r"\w+", flags=re.UNICODE)
CLOZE_RE = re.compile(r"_.+_")

def count_words(text: str) -> int:
    words = len(WORD_RE.findall(text))
    return words

def estimate_tokens(text: str) -> int:
    words = len(WORD_RE.findall(text))
    return max(1, int(words / 0.75))

def filter_valid_cloze_lines(text: str) -> List[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip() and CLOZE_RE.search(ln)]
