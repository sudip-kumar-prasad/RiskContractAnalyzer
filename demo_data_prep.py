import argparse
import sys
from src.data_preprocessing.document_loader import load_text_from_file
from src.data_preprocessing.text_cleaner import clean_text
from src.data_preprocessing.segmenter import segment_into_clauses

def main():
    parser = argparse.ArgumentParser(description="Test Data Preprocessing Pipeline")
    parser.add_argument('filepath', type=str, help="Path to a .txt or .pdf file containing a contract")
    
    args = parser.parse_args()
    filepath = args.filepath
    
    print(f"Loading document from: {filepath}...")
    try:
        raw_text = load_text_from_file(filepath)
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)
        
    print(f"\nDocument loaded successfully. Extracted {len(raw_text)} characters.")
    print("-" * 50)
    
    print("Segmenting into clauses...")
    clauses = segment_into_clauses(raw_text)
    print(f"Found {len(clauses)} potential clauses.")
    print("-" * 50)
    
    print("Preprocessing top 5 clauses:")
    for i, clause in enumerate(clauses[:5], 1):
        cleaned = clean_text(clause)
        print(f"\nClause {i} (Raw):")
        print(f"  {clause[:150]}{'...' if len(clause)>150 else ''}")
        print(f"Clause {i} (Cleaned for ML):")
        print(f"  {cleaned[:150]}{'...' if len(cleaned)>150 else ''}")

if __name__ == "__main__":
    main()
