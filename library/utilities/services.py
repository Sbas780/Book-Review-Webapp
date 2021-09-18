from library.adapters.memory_repository import AbstractRepository


def get_books(repo: AbstractRepository):
    books = repo.get_books()
    return books

def get_number_of_books(repo: AbstractRepository):
    number_of_boooks = repo.get_number_of_books()
    return number_of_boooks

