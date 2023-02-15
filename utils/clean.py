import re

def clean_text(text):
    """
        This function removes unwanted characters from the text
    """
    text = re.sub(r'\b\w+\b[^.!?]*$', '', text)
    text = re.sub(r'(?:^|[.!?])\s*\w*(?:bets|Bets)\w*\s*[.!?]', '', text)
    return text.strip()

