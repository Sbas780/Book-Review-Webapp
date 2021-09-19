from flask import Blueprint, render_template, redirect, request

import library.utilities.utilities as utils
from .services import search_for_items
from library.forms.forms import RequiredForms



search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    form = RequiredForms(request.args, meta={'csrf': False})
    books = utils.get_list_of_books()
    if search == 'POST':
        return render_template('search.html', form=form, book_list=books)
    query = request.args.get('search', '')

    if query == "":
        utils.set_search_results(books)
    books = search_for_items(query)
    return render_template('search.html', form=form, book_list=books)




