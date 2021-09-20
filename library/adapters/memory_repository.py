from pathlib import Path
from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import *
from library.adapters.jsondatareader import BooksJSONReader
import json

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__authors = list()
        self.__users = list()
        self.__search_results = list()
        self.__publishers = list()
        self.__available_author = list()

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

    def get_users(self) -> list[User]:
        return self.__users

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name: User):
        return next((user for user in self.__users if user.user_name == user_name), None)

    def has_book(self, author: Author) -> bool:
        for book in self.__books:
            if author in book.authors:
                return True
        return False

    def get_search_results(self):
        return self.__search_results

    def set_search_results(self, array):
        self.__search_results = array

    def clear_search_results(self):
        self.__search_results = []

    def get_publishers(self) -> list[Publisher]:
        for book in self.__books:
            if book.publisher not in self.__publishers and book.publisher.name != "N/A":
                self.__publishers.append(book.publisher)
        return self.__publishers

    def get_available_authors(self):
        for book in self.__books:
            for author in book.authors:
                if author not in self.__available_author:
                    self.__available_author.append(author)
        return self.__available_author


    def get_book_by_id(self, book_id):
        for book in self.__books:
            if str(book.book_id) == book_id:
                return book















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