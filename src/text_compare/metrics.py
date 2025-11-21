import math
import spacy
import textstat
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from collections import Counter
import numpy as np
from scipy.stats import entropy
import subprocess
import sys

# -------------------------------
# 0️⃣ Load spaCy and GPT-2
# -------------------------------
def get_spacy_model(model_name="en_core_web_sm"):
    try:
        return spacy.load(model_name)
    except OSError:
        print(f"Model '{model_name}' not found. Downloading...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        return spacy.load(model_name)

nlp = get_spacy_model()

# GPT-2 loaded but used only for single texts, not genre stats
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()
if torch.cuda.is_available():
    model.to("cuda")

# -------------------------------
# 1️⃣ Lexical and syntactic metrics (use doc directly)
# -------------------------------
def compute_ttr_doc(doc):
    tokens = [t.text.lower() for t in doc if t.is_alpha]
    if not tokens:
        return 0
    return len(set(tokens)) / len(tokens)

def sentence_length_stats_doc(doc):
    lengths = [len(sent) for sent in doc.sents]
    if not lengths:
        return 0, 0
    return np.mean(lengths), np.std(lengths)

def pos_entropy_doc(doc):
    pos_tags = [t.pos_ for t in doc if t.is_alpha]
    if not pos_tags:
        return 0
    counts = Counter(pos_tags)
    probs = np.array(list(counts.values())) / sum(counts.values())
    return entropy(probs)

def lexical_density_doc(doc):
    content_words = [t for t in doc if t.pos_ in {"NOUN", "VERB", "ADJ", "ADV"}]
    words = [t for t in doc if t.is_alpha]
    return len(content_words) / len(words) if words else 0

def avg_word_length_doc(doc):
    words = [t.text for t in doc if t.is_alpha]
    lengths = [len(w) for w in words]
    return np.mean(lengths) if lengths else 0

# -------------------------------
# 2️⃣ Readability (text-based)
# -------------------------------
def readability_score(text):
    return textstat.flesch_reading_ease(text)

# -------------------------------
# 3️⃣ GPT-2 Perplexity (use only for user input)
# -------------------------------
def compute_perplexity(text, max_len=512):
    tokens = tokenizer.encode(text, return_tensors="pt")
    if tokens.size(1) > max_len:
        tokens = tokens[:, :max_len]
    if torch.cuda.is_available():
        tokens = tokens.to("cuda")
    with torch.no_grad():
        outputs = model(tokens, labels=tokens)
        loss = outputs.loss.item()
        return math.exp(loss)

# -------------------------------
# 4️⃣ Aggregate function for genre stats
# -------------------------------
def extract_text_features_for_genre(text):
    """
    Fast feature extraction for genre stats.
    GPT-2 perplexity is excluded for speed.
    """

    doc = nlp(text)
    features = {
        "ttr": compute_ttr_doc(doc),
        "lexical_density": lexical_density_doc(doc),
        "avg_word_length": avg_word_length_doc(doc),
        "mean_sentence_length": sentence_length_stats_doc(doc)[0],
        "std_sentence_length": sentence_length_stats_doc(doc)[1],
        "pos_entropy": pos_entropy_doc(doc),
        "readability_flesch_kincaid": readability_score(text),
        # "perplexity_gpt2" excluded for batch processing
    }
    return features

# -------------------------------
# 5️⃣ Aggregate function for single user text
# -------------------------------
def extract_text_features(text):
    """
    Full extraction including GPT-2 perplexity.
    Intended for single texts (user input).
    """
    doc = nlp(text)
    features = {
        "ttr": compute_ttr_doc(doc),
        "lexical_density": lexical_density_doc(doc),
        "avg_word_length": avg_word_length_doc(doc),
        "mean_sentence_length": sentence_length_stats_doc(doc)[0],
        "std_sentence_length": sentence_length_stats_doc(doc)[1],
        "pos_entropy": pos_entropy_doc(doc),
        "readability_flesch_kincaid": readability_score(text),
        "perplexity_gpt2": compute_perplexity(text),
    }
    return features
