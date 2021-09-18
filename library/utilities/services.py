from library.adapters.memory_repository import AbstractRepository


def get_books(repo: AbstractRepository):
    books = repo.get_books()
    return books

def get_number_of_books(repo: AbstractRepository):
    number_of_books = repo.get_number_of_books()
    return number_of_books

def get_authors_list(repo: AbstractRepository):
    authors = repo.get_authors()
    return authors