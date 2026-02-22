"""
Train Logistic Regression and Decision Tree classifiers.
"""
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from src.model_training.config import RANDOM_STATE


def train_models(X_train_vec, y_train) -> dict:
    """
    Train both classifiers on the vectorized training data.

    Args:
        X_train_vec: Sparse TF-IDF matrix for training split.
        y_train: Binary labels (1 = Risky, 0 = Safe).

    Returns:
        Dict mapping model name to fitted model instance.
    """
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced"
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=10, random_state=RANDOM_STATE, class_weight="balanced"
        ),
    }
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train_vec, y_train)
    return models
