"""
utils/clause_segmenter.py
--------------------------
Wraps the existing segmenter logic and adds structured output with
clause IDs and character counts suitable for Streamlit display.
"""

import re
import sys
import os
from typing import List, Dict

# Allow importing from src/ even when running from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from src.data_preprocessing.segmenter import segment_into_clauses as _core_segment
    _USE_CORE = True
except ImportError:
    _USE_CORE = False


def _fallback_segment(text: str) -> List[str]:
    """
    Simple fallback clause segmenter in case the src module is unavailable.
    Splits on double newlines and then on numbered list starters.
    """
    if not text:
        return []

    paragraphs = re.split(r"\n\s*\n", text)
    clauses = []
    delimiter_pattern = r"(?m)(^\s*\d+\.\d*\s*|^\s*[a-zA-Z]\)\s*|^\s*[ivxIVX]+\.\s*)"

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        parts = re.split(delimiter_pattern, para)
        current = ""
        for part in parts:
            if re.match(delimiter_pattern, part):
                if current.strip():
                    clauses.append(current.strip())
                current = part
            else:
                current += part
        if current.strip():
            clauses.append(current.strip())

    return [c for c in clauses if len(c.split()) > 3]


def segment_document(text: str) -> List[Dict]:
    """
    Segments the raw contract text into a list of clause dicts.

    Each dict contains:
        - id          (int)   : 1-based clause index
        - text        (str)   : the clause text
        - word_count  (int)   : number of words in the clause

    Args:
        text (str): Raw contract text.

    Returns:
        List of clause dicts.
    """
    if _USE_CORE:
        raw_clauses = _core_segment(text)
    else:
        raw_clauses = _fallback_segment(text)

    structured = []
    for idx, clause_text in enumerate(raw_clauses, start=1):
        structured.append(
            {
                "id": idx,
                "text": clause_text,
                "word_count": len(clause_text.split()),
            }
        )

    return structured
