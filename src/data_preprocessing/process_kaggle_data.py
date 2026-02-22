import os
import pandas as pd

def process_kaggle_dataset(input_csv_path: str, output_csv_path: str):
    """
    Reads the raw Kaggle dataset ('legal_docs_modified.csv'),
    cleans up missing values or unnecessary columns, and maps the columns
    to match the ML training script's expected schema (clause_text, is_risky).
    """
    if not os.path.exists(input_csv_path):
        raise FileNotFoundError(f"Input dataset not found at {input_csv_path}. Please download it first.")

    print(f"Loading Kaggle dataset from {input_csv_path}...")
    df = pd.read_csv(input_csv_path)

    # Standardize column names based on the dump format:
    # 'clause_text' is the text.
    # 'clause_status' appears to be the binary label (0 for safe, 1 for risky/flagged).
    
    if 'clause_text' not in df.columns or 'clause_status' not in df.columns:
        raise ValueError("The dataset does not contain required 'clause_text' or 'clause_status' columns.")

    # Drop nulls
    df = df.dropna(subset=['clause_text', 'clause_status'])

    # Ensure status is an integer (0 or 1)
    df['clause_status'] = df['clause_status'].astype(int)

    # Filter to only keep our necessary columns and rename them to standard format 
    # expected by our ML training pipeline.
    cleaned_df = df[['clause_text', 'clause_status']].rename(columns={
        'clause_status': 'is_risky'
    })

    print(f"Processed dataset: {len(cleaned_df)} rows.")
    print(f"Class distribution:\n{cleaned_df['is_risky'].value_counts()}")

    # Save to processed folder
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    cleaned_df.to_csv(output_csv_path, index=False)
    print(f"Saved processed dataset to {output_csv_path}.")

if __name__ == "__main__":
    input_file = "data/raw/legal_docs_modified.csv"
    output_file = "data/processed/kaggle_training_data.csv"
    process_kaggle_dataset(input_file, output_file)
