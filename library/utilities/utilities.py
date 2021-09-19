import library.adapters.repository as repo
import library.utilities.services as services

def get_list_of_books():
    books = services.get_books(repo.repo_instance)
    return books

def get_number_of_books():
    number_of_books = services.get_number_of_books(repo.repo_instance)
    return number_of_books

def get_authors():
    authors = services.get_authors_list(repo.repo_instance)
    return authors

def set_search_results(array):
    services.set_search_results(repo.repo_instance, array)

def get_search_results():
    return services.get_search_results(repo.repo_instance)

def clear_search_results():
    services.clear_search_results(repo.repo_instance)

def get_publishers():
    return services.get_publishers(repo.repo_instance)