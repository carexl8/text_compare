import streamlit as st
import pandas as pd
from load_data import load_genre_stats
from text_compare.compute_stats import compute_genre_stats
from compute_features import compute_features

st.set_page_config(page_title="Stylistic Statistics", layout="wide")
st.title("📄 Text Feature Comparison")
st.write("Upload or paste a text to compare it against genre averages.")

# --- CACHING GENRE STATS ---
@st.cache_data
def get_genre_stats():
    """
    Load precomputed genre stats or compute them if missing.
    """
    try:
        return load_genre_stats()
    except FileNotFoundError:
        return compute_genre_stats()

genre_stats = get_genre_stats()

# --- TEXT INPUT ---
tab1, tab2 = st.tabs(["Paste text", "Upload .txt"])
user_text = ""

with tab1:
    user_text = st.text_area("Enter text:", height=250)

with tab2:
    uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded:
        user_text = uploaded.read().decode("utf-8")

# --- GENRE SELECTION AND FEATURE COMPARISON ---
if user_text:
    genres = list(genre_stats.index)
    selected_genre = st.selectbox("Choose a genre to compare your text to:", genres)

    if st.button("Compute Features & Compare"):
        # --- COMPUTE FEATURES WITH SPINNER ---
        with st.spinner("Computing text features…"):
            features = compute_features(user_text)

        # --- BUILD COMPARISON TABLE ---
        feature_names = {
            "ttr": "Type-Token Ratio",
            "lexical_density": "Lexical Density",
            "avg_word_length": "Average Word Length",
            "mean_sentence_length": "Mean Sentence Length",
            "std_sentence_length": "Std Sentence Length",
            "pos_entropy": "POS Entropy",
            "readability_flesch_kincaid": "Readability (Flesch)",
            "perplexity_gpt2": "GPT-2 Perplexity"
        }

        table_data = []
        for key, label in feature_names.items():
            # Safe access: use None if column is missing in genre_stats or feature
            avg_value = genre_stats.loc[selected_genre, key] if key in genre_stats.columns else None
            user_value = features.get(key, None)

            table_data.append({
                "Feature": label,
                "Average for Genre": avg_value,
                "Your Text": user_value
            })

        comparison_df = pd.DataFrame(table_data)

        st.subheader("Comparison Table")
        st.dataframe(comparison_df)

else:
    st.info("Awaiting text input...")