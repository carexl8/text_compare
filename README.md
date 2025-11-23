# Stylistic Text Comparison

This project allows users to compare an input English text against genre-specific averages (e.g., TTR, perplexity) computed from the AMALGUM corpus. This is a work in progress, and I will be updating the repo incrementally.

## Features

- Upload or paste text
- Compute lexical, syntactic, readability, and GPT-2 perplexity features
- Compare against genre averages

## Folder Structure
```
text_compare/
├── app/ # Streamlit app
├── data/ # Raw and processed datasets
├── src/ # Python modules (metrics, compute_stats)
├── requirements.txt # Python dependencies
├── README.md
```

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

### 1. Download AMALGUM

AMALGUM is available on GitHub:

**[https://github.com/gucorpling/amalgum](https://github.com/gucorpling/amalgum)**

Download the repository (or clone it):

```
git clone https://github.com/gucorpling/amalgum.git
```


### 2. Copy the `.conllu` files into the project

Place all `.conllu` files into:

```
data/raw/amalgum/
```

Your folder should look like:

```
data/
 └── raw/
     └── amalgum/
         ├── amalgum_academic.conllu
         ├── amalgum_biography.conllu
         ├── ...
```

### 3. Process genre statistics

The first time you run the project, you may need to generate summary stats:

```
data/processed/genre_stats.pkl
```

These are created automatically by running:

```
python src/text_compare/compute_stats.py
```

If the file already exists, you don’t need to regenerate it.


## License

MIT

