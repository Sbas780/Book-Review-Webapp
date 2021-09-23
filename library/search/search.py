from flask import Blueprint, render_template, redirect, request
from library.search.services import create_search_fields
import library.utilities.utilities as utils
import library.adapters.repository as repo
from .services import search_for_items




search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search(page_number=0):
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

    book_chunks = utils.get_chunks(books, 10)

    page_number = request.args.get("page_number")
    if page_number is None:
        page_number = 0

    page_number = int(page_number)
    if page_number == 0:
        previous_page = 0
    else:
        previous_page = page_number - 1

    if page_number == len(book_chunks) - 1:
        next_page = len(book_chunks) - 1
    else:
        next_page = page_number + 1


    return render_template('search.html',
                           url_route="search_bp.search",
                           current_page=page_number,
                           prev_page=previous_page,
                           next_page=next_page,
                           num_pages=len(book_chunks),
                           form=form, book_list=book_chunks[page_number])




