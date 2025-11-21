import os
import subprocess
import shutil

def clone_amalgum_repo(dest_dir="../data/raw/amalgum"):
    """
    Clone the AMALGUM corpus from GitHub if it doesn't exist locally.
    AMALGUM = Annotated Multilayer Corpus of American English
    (contains multiple genres, modern English texts).
    """

    repo_url = "https://github.com/gucorpling/amalgum.git"

    if os.path.exists(dest_dir):
        print(f"[info] Dataset already exists at {dest_dir}. Skipping clone.")
        return

    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)

    print(f"[download] Cloning AMALGUM from {repo_url} → {dest_dir}")
    try:
        subprocess.run(["git", "clone", repo_url, dest_dir], check=True)
        print("[success] AMALGUM successfully cloned.")
    except subprocess.CalledProcessError as e:
        print("[error] Failed to clone AMALGUM repository.")
        print(e)

def clean_amalgum_repo(dest_dir="../data/raw/amalgum"):
    """
    Remove unnecessary Git files to save space (optional).
    """
    git_dir = os.path.join(dest_dir, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
        print("[cleanup] Removed .git folder to save space.")

def main():
    clone_amalgum_repo()
    clean_amalgum_repo()

if __name__ == "__main__":
    main()
