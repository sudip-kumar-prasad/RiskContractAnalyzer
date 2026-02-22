"""
Configuration constants for the ML training pipeline.
"""
import os

# Train/test split parameters
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Directory where trained models will be saved
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

# Output filenames
BEST_MODEL_FILENAME = "best_model.joblib"
VECTORIZER_FILENAME = "vectorizer.joblib"
