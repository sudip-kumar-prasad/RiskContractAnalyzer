"""
Persist the best model and the fitted TF-IDF vectorizer to disk.
"""
import os
import joblib
from src.model_training.config import (
    MODELS_DIR, BEST_MODEL_FILENAME, VECTORIZER_FILENAME
)


def save_best(models: dict, best_name: str, vectorizer) -> None:
    """
    Save the best classifier and the fitted vectorizer using joblib.

    Args:
        models: Dict mapping model name to fitted sklearn estimator.
        best_name: Key in `models` identifying the best model.
        vectorizer: Fitted TfidfVectorizer instance.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)

    model_path = os.path.join(MODELS_DIR, BEST_MODEL_FILENAME)
    vec_path = os.path.join(MODELS_DIR, VECTORIZER_FILENAME)

    joblib.dump(models[best_name], model_path)
    joblib.dump(vectorizer, vec_path)

    print(f"\nSaved model     → {model_path}")
    print(f"Saved vectorizer → {vec_path}")
