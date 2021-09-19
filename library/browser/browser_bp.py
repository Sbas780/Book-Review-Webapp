from flask import Blueprint, render_template, request
from library.forms.forms import RequiredForms

import library.utilities.utilities as utils
import library.adapters.repository as repo
from library.browser import services

browser_bp = Blueprint('browser_bp', __name__, url_prefix='/browsing')

@browser_bp.route('/books', methods=['GET', 'POST'])
def browse_books():
    form = RequiredForms(request.args, meta={'csrf': False})
    books = utils.get_list_of_books()
    select = request.args.get("sort")
    query = request.args.get('search', '')
    if select == "2":
        results = services.get_search_results()
        results = services.sort_by_date(results)
        return render_template('books.html', book_list=results, form=form)

    return render_template('books.html', book_list=books, form=form)

@browser_bp.route('/authors', methods=['GET'])
def browse_authors():
    authors = utils.get_authors()
    return render_template('authors.html', author_list=authors)



