from pathlib import Path
from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import *

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()

    def get_books(self) -> list[Book]:
        return self.__books

    def add_book(self, book: Book):
        self.__books.append(book)

book1 = Book(1234, "Book1")
book2 = Book(5678, "Book2")

def load_books(repo: MemoryRepository):
    repo.add_book(book1)
    repo.add_book(book2)


def populate(data_path: Path, repo: MemoryRepository):
    load_books(repo)