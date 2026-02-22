import re
from typing import List

def segment_into_clauses(text: str) -> List[str]:
    """
    Segments a full contract text into individual clauses.
    This uses a basic heuristic approach to split by common clause delimiters
    like numbered lists (1., 2.), bullet points, or double newlines.

    Args:
        text (str): The full raw text of the contract.

    Returns:
        List[str]: A list of segmented clauses.
    """
    if not text:
        return []

    # Strategy 1: Split by double newlines (paragraphs)
    # Often, distinct clauses are separated by empty lines.
    paragraphs = re.split(r'\n\s*\n', text)
    
    clauses = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # Strategy 2: Further split by numbering (e.g., "1.", "1.1", "a)") if they appear inside a paragraph
        # This regex looks for a newline/start followed by numbers/letters and a dot or parenthesis
        # Example: "\n 1. " or "^a) "
        # We replace these delimiters with a special marker to split easily
        
        # This is a simple regex for demonstration. Complex legal documents might need more robust parsing.
        delimiters = r'(?m)(^\s*\d+\.\d*\s*|^\s*[a-z]\)\s*|^\s*[ivx]+\.\s*)'
        
        # Split the paragraph by these delimiters
        parts = re.split(delimiters, para)
        
        # Reconstruct the clauses
        current_clause = ""
        for i, part in enumerate(parts):
            if re.match(delimiters, part):
                # If we have an existing clause, save it before starting a new one
                if current_clause:
                    clauses.append(current_clause.strip())
                current_clause = part # Start new clause with its delimiter
            else:
                current_clause += part
                
        if current_clause:
            clauses.append(current_clause.strip())

    # Filter out very short strings that are likely not real clauses
    final_clauses = [c for c in clauses if len(c.split()) > 3]
    
    return final_clauses
