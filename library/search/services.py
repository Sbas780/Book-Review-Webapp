from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField

import library.utilities.utilities as utils
from library.adapters.repository import AbstractRepository
from library.utilities.services import get_available_authors, get_publishers

def search_for_items(user_input: str, authors, publishers):
    book_results = []
    user_input = user_input.lower()
    books = utils.get_list_of_books()

    for book in books:
        if user_input in str(book.book_id) or user_input in book.title.lower() or user_input in book.publisher.name.lower():
            book_results.append(book)

    if publishers:
        book_results = filter(lambda x: any(publisher == x.publisher.name for publisher in publishers), book_results)


    return book_results


def create_search_fields(repo: AbstractRepository, request_args):
    publishers = get_publishers(repo)
    authors = get_available_authors(repo)
    form = SearchForm(request_args)
    form.publisher.choices = [(publisher.name, publisher.name) for publisher in publishers] + [('', 'Publishers')]
    form.author.choices = [(author.full_name, author.full_name) for author in authors] + [('', 'Authors')]
    return form



class SearchForm(FlaskForm):
    search = StringField("search")
    publisher = SelectMultipleField("Publishers")
    author = SelectMultipleField("Authors")
    submit = SubmitField("Find")
