import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Setup NLTK resources
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
# Ensure punkt_tab is downloaded if needed by newer nltk versions
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

def clean_text(text: str) -> str:
    """
    Cleans the input text by:
    - Lowercasing
    - Removing special characters, punctuation, and extra whitespace
    - Removing stopwords

    Args:
        text (str): The raw text to clean.

    Returns:
        str: The cleaned text.
    """
    if not text:
        return ""
    
    # Lowercase the text
    text = text.lower()
    
    # Remove special characters and punctuation (keep alphanumeric and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back into a single string
    cleaned_text = ' '.join(cleaned_tokens)
    
    # Remove extra spaces that might be left
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text
