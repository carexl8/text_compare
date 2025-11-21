import glob
import os
import re
import pandas as pd
from joblib import Parallel, delayed
from .metrics import extract_text_features_for_genre

def extract_text_from_conllu(file_path):
    """Extracts plain text from a .conllu file"""
    lines = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("# text = "):
                lines.append(line.replace("# text = ", "").strip())
    return " ".join(lines)

def extract_genre_from_conllu(file_path):
    """Extract genre from '# newdoc id = AMALGUM_<genre>_<doc>'"""
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("# newdoc id ="):
                match = re.search(r"AMALGUM_([a-zA-Z]+)_", line)
                if match:
                    return match.group(1)
    return None

def compute_genre_stats():
    """Compute average features per genre in parallel"""
    # ---- Paths ----
    PROJECT_ROOT = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    RAW_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "amalgum")
    PROCESSED_PATH = os.path.join(PROJECT_ROOT, "data", "processed")
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    # ---- Collect files ----
    files = glob.glob(os.path.join(RAW_PATH, "**", "*.conllu"), recursive=True)
    print("Files found:", len(files))

    if not files:
        raise RuntimeError(f"No .conllu files found in {RAW_PATH}")

    # ---- Parallel feature extraction ----
    def process_file(f):
        genre = extract_genre_from_conllu(f)
        if genre is None:
            print(f"⚠️ Skipping file (no genre found): {os.path.basename(f)}")
            return None
        text = extract_text_from_conllu(f)[:200]  # snippet for speed
        features = extract_text_features_for_genre(text)
        features["genre"] = genre
        return features

    results = Parallel(n_jobs=-1, backend="loky")(
        delayed(process_file)(f) for f in files
    )

    # Remove None results
    results = [r for r in results if r is not None]
    if not results:
        raise RuntimeError("No valid files processed — check your data paths.")

    # ---- Build DataFrame and compute genre averages ----
    df = pd.DataFrame(results)
    genre_stats = df.groupby("genre").mean(numeric_only=True)

    # ---- Save to disk ----
    out_path = os.path.join(PROCESSED_PATH, "genre_stats.pkl")
    genre_stats.to_pickle(out_path)
    print(f"✅ Genre statistics saved to {out_path}")

    return genre_stats
