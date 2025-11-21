from text_compare.metrics import extract_text_features


def compute_features(text: str) -> dict:
    """Compute feature dictionary from raw text."""
    return extract_text_features(text)
