from library.adapters.memory_repository import AbstractRepository


def get_books(repo: AbstractRepository):
    books = repo.get_books()
    return books
