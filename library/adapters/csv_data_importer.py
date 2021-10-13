from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import *
from library.adapters.jsondatareader import BooksJSONReader
from pathlib import Path

import json
import csv


def read_csv_file(filename: str):
    with open(filename, encoding="utf-8-sig") as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:  
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_books(data_path: Path, repo: AbstractRepository):
    authors = str(data_path / "book_authors_excerpt.json")
    comic_books = str(data_path / "comic_books_excerpt.json")
    reader_instance = BooksJSONReader(comic_books, authors)
    reader_instance.read_json_files()
    for book in reader_instance.dataset_of_books:
        repo.add_publisher(book.publisher)
        repo.add_book(book)



def load_authors(data_path: Path, repo: AbstractRepository):
    authors_file = str(data_path / "book_authors_excerpt.json")
    file = open(authors_file)
    authors_file_content = file.readlines()
    for authors in authors_file_content:
        temp_dict = json.loads(authors)
        new_author = Author(int(temp_dict["author_id"]), temp_dict["name"])
        repo.add_author(new_author)


def load_users(data_path: Path, repo: AbstractRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(user_name=data_row[1], password=generate_password_hash(data_row[2]))
        repo.add_user(user)
        users[data_row[0]] = user
    return users
