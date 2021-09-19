from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField

import library.utilities.utilities as utils
from library.adapters.repository import AbstractRepository
from library.utilities.services import get_available_authors, get_publishers

def search_for_items(user_input: str):
    book_results = []
    user_input = user_input.lower()
    books = utils.get_list_of_books()

    if user_input == "":
        return books
    for book in books:
        if user_input in str(book.book_id):
            if book not in book_results:
                book_results.append(book)

        if user_input in book.title.lower():
            if book not in book_results:
                book_results.append(book)

        if user_input in book.publisher.name.lower():
            if book not in book_results:
                book_results.append(book)

    utils.set_search_results(book_results)
    return book_results


def create_search_fields(repo: AbstractRepository, request_args):
    publishers = get_publishers(repo)
    authors = get_available_authors(repo)
    form = SearchForm(request_args)
    form.publisher.choices = [(publisher.name, publisher.name) for publisher in publishers] + [('', 'Publisher')]
    form.author.choices = [(author.full_name, author.full_name) for author in authors]
    return form



class SearchForm(FlaskForm):
    search = StringField("search")
    publisher = SelectMultipleField("Publisher")
    author = SelectMultipleField("Author")
    submit = SubmitField("Find")
