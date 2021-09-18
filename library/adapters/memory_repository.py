from pathlib import Path
from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import *
from library.adapters.jsondatareader import BooksJSONReader
import json

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__authors = list()

    def get_books(self) -> list[Book]:
        return self.__books

    def add_book(self, book: Book):
        self.__books.append(book)

    def get_authors(self):
        return self.__authors

    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_number_of_books(self) -> int:
        return len(self.__books)

def load_books(data_path: Path, repo: MemoryRepository):
    authors = str(data_path / 'book_authors_excerpt.json')
    comic_books = str(data_path / 'comic_books_excerpt.json')
    reader_instance = BooksJSONReader(comic_books, authors)
    reader_instance.read_json_files()
    for book in reader_instance.dataset_of_books:
        repo.add_book(book)

def load_authors(data_path: Path, repo: AbstractRepository):
    authors_file = str(data_path / 'book_authors_excerpt.json')
    file = open(authors_file)
    authors_file_content = file.readlines()
    for authors in authors_file_content:
        temp_dict = json.loads(authors)
        new_author = Author(int(temp_dict["author_id"]), temp_dict["name"])
        repo.add_author(new_author)



def populate(data_path: Path, repo: MemoryRepository):
    load_authors(data_path, repo)
    load_books(data_path, repo)