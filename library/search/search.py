from flask import Blueprint, render_template, redirect, request
from library.search.services import create_search_fields
import library.utilities.utilities as utils
import library.adapters.repository as repo
from .services import search_for_items




search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    form = create_search_fields(repo.repo_instance, request.args)
    books = utils.get_list_of_books()
    if search == 'POST':
        return render_template('search.html', form=form, book_list=books)
    query = request.args.get('search', '')
    authors = request.args.getlist('author')
    publishers = request.args.getlist('publisher')
    years = request.args.getlist('year')
    ebook = request.args.get('ebook')
    books = search_for_items(query, authors, publishers, years, ebook)
    return render_template('search.html', form=form, book_list=books)




