# Stylistic Text Comparison

This project allows users to compare an input English text against genre-specific averages (e.g., TTR, perplexity) computed from the AMALGUM corpus. This is a work in progress, and I will be updating the repo incrementally.

## Features

- Upload or paste text
- Compute lexical, syntactic, readability, and GPT-2 perplexity features
- Compare against genre averages

## Folder Structure

01/

├── app/ # Streamlit app

├── data/ # Raw and processed datasets

├── src/ # Python modules (metrics, compute_stats)

├── requirements.txt # Python dependencies

├── README.md

## Setup

### 1. Create and activate a conda environment (optional but recommended)

```
conda create -n txt_compare python=3.12 pip
conda activate txt_compare
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. (Recommended) Install the package in editable mode

This ensures Python correctly finds the `src/` modules:

```
pip install -e .
```

### 4. Run the Streamlit app

```
streamlit run app/main.py
```

## Data

Place .conllu files in data/raw/amalgum/

Processed genre statistics are saved to data/processed/genre_stats.pkl

## License

MIT

