# Stylistic Text Comparison

This project allows users to compare an input English text against genre-specific averages (e.g., TTR, perplexity) computed from the AMALGUM corpus.

## Features

- Upload or paste text
- Compute lexical, syntactic, readability, and GPT-2 perplexity features
- Compare against genre averages
- Visualize closest matching genre

## Folder Structure

01/
├── app/ # Streamlit app
├── data/ # Raw and processed datasets
├── src/ # Python modules (metrics, compute_stats)
├── requirements.txt # Python dependencies
├── README.md

## Setup

1. Create a conda environment (optional):
```bash
conda create -n txt_compare python=3.12
conda activate txt_compare

    Install dependencies:

pip install -r requirements.txt

    Run the app:

streamlit run app/main.py

## Data

    Place .conllu files in data/raw/amalgum/

    Processed genre statistics are saved to data/processed/genre_stats.pkl

## License

MIT

