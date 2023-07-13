"""Configuration for the project."""
from pathlib import Path

# Folder structure
PROJECT_ROOT = [p for p in Path(__file__).parents if p / '.git' in p.iterdir()][0]
DATA_FOLDER = PROJECT_ROOT / 'data'
DATA_FOLDER.mkdir(exist_ok=True)
