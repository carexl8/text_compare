import pandas as pd
import os

def load_genre_stats(filename="genre_stats.pkl"):
    """
    Load precomputed genre averages from data/processed
    Works no matter where the script is run from.
    """
    # Project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(project_root, "data", "processed", filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    return pd.read_pickle(path)
