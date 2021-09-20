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

def set_search_results(repo: AbstractRepository, search_results: []):
    repo.set_search_results(search_results)

def get_search_results(repo: AbstractRepository):
    return repo.get_search_results()

def clear_search_results(repo: AbstractRepository):
    repo.clear_search_results()

def get_publishers(repo: AbstractRepository):
    return repo.get_publishers()

def get_available_authors(repo: AbstractRepository):
    return repo.get_available_authors()


def get_book_by_id(repo: AbstractRepository, book_id):
    return repo.get_book_by_id(book_id)
