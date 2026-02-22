import os
import PyPDF2

def load_text_from_file(file_path: str) -> str:
    """
    Reads text data from a PDF or TXT file.
    Args:
        file_path (str): The path to the file.
    Returns:
        str: The extracted text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} was not found.")

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    elif file_extension == '.pdf':
        text = ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text
    
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Only .txt and .pdf are supported.")
