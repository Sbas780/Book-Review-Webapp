
from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.csv_data_importer import load_comments, load_users, load_articles_and_tags

def populate(data_path: Path, repo: MemoryRepository):
    load_authors(data_path, repo)
    load_books(data_path, repo)
    load_users(data_path, repo)