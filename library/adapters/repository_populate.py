
from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.csv_data_importer import load_authors, load_users, load_books

def populate(data_path: Path, repo: AbstractRepository, database_mode):
    #load_authors(data_path, repo)
    #load_books(data_path, repo)
    load_users(data_path, repo)