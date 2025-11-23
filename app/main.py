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

genres = list(genre_stats.index)
selected_genre = st.selectbox("Choose a genre to compare your text to:", genres)

if st.button("Compute Features & Compare"):
    # --- COMPUTE FEATURES WITH SPINNER ---
    with st.spinner("Computing text features…"):
        features = compute_features(user_text)

    # --- METRIC EXPLANATIONS (TABS) ---
    st.subheader("Statistics and Explanations")

    feature_names = {
        "ttr": "Type-Token Ratio",
        "lexical_density": "Lexical Density",
        "avg_word_length": "Average Word Length",
        "mean_sentence_length": "Mean Sentence Length",
        "std_sentence_length": "Standard Deviation Sentence Length",
        "pos_entropy": "Part of Speech Entropy",
        "readability_flesch_kincaid": "Readability (Flesch)",
        "perplexity_gpt2": "GPT-2 Perplexity"
    }

    descriptions = {
        "ttr": """
**What it measures:**  
The proportion of unique words (types) relative to total words (tokens).

**Higher value:** More lexical variety, richer vocabulary.  
**Lower value:** More repetition, less lexical diversity.
""",
        "lexical_density": """
**What it measures:**  
The percentage of content words (nouns, verbs, adjectives, adverbs).

**Higher value:** More information-dense, academic or technical style.  
**Lower value:** More conversational, narrative, or functional language.
""",
        "avg_word_length": """
**What it measures:**  
The mean number of characters per word.

**Higher value:** More complex vocabulary.  
**Lower value:** Simpler, more accessible language.
""",
        "mean_sentence_length": """
**What it measures:**  
The average number of words per sentence.

**Higher value:** More complex, multi-clause sentences.  
**Lower value:** Short, simple, direct sentences.
""",
        "std_sentence_length": """
**What it measures:**  
Variation in sentence length.

**Higher value:** Mix of long and short sentences; stylistic variation.  
**Lower value:** Uniform sentence lengths; more controlled or formulaic style.
""",
        "pos_entropy": """
**What it measures:**  
The diversity of part-of-speech categories in the text.

**Higher value:** Greater syntactic variety.  
**Lower value:** More uniform, predictable syntactic structure.
""",
        "readability_flesch_kincaid": """
**What it measures:**  
Flesch-Kincaid readability score estimating grade level needed to understand the text.

**Higher value:** Easier to read; simpler vocabulary and grammar.  
**Lower value:** Harder to read; more complex text.
""",
        "perplexity_gpt2": """
**What it measures:**  
How predictable the text is to a GPT-2 language model.

**Higher value:** More surprising, less typical text; possibly more errors.  
**Lower value:** More fluent, predictable, natural text.
"""
    }

    # Create tabs
    tabs = st.tabs(list(feature_names.values()))

    for key, tab in zip(feature_names.keys(), tabs):
        with tab:
            avg_value = genre_stats.loc[selected_genre, key] if key in genre_stats.columns else None
            user_value = features.get(key, None)

            # Round numeric values to 2 decimals
            if isinstance(avg_value, (int, float)):
                avg_value = round(avg_value, 2)
            if isinstance(user_value, (int, float)):
                user_value = round(user_value, 2)

            st.markdown(f"**Average for the genre:** {avg_value}")
            st.markdown(f"**Value for your text:** {user_value}\n")
            st.markdown(descriptions[key])
