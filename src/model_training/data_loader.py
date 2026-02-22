"""
Data loading and train/test splitting for the ML classifier pipeline.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from src.model_training.config import TEST_SIZE, RANDOM_STATE


def load_and_split(df: pd.DataFrame):
    """
    Validate the DataFrame and split into train/test sets.

    Args:
        df: DataFrame with 'clause_text' (str) and 'is_risky' (int 0/1) columns.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test).
    """
    required = {"clause_text", "is_risky"}
    if not required.issubset(df.columns):
        raise ValueError(f"DataFrame must contain columns: {required}")

    X = df["clause_text"].astype(str)
    y = df["is_risky"].astype(int)

    return train_test_split(X, y, test_size=TEST_SIZE,
                            random_state=RANDOM_STATE, stratify=y)
