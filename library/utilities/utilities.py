import library.adapters.repository as repo
import library.utilities.services as services

def get_list_of_books():
    books = services.get_books(repo.repo_instance)
    return books
