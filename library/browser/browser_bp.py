from flask import Blueprint, render_template, request

import library.utilities.utilities as utils
import library.adapters.repository as repo
from library.browser import services

browser_bp = Blueprint('browser_bp', __name__, url_prefix='/browsing')

@browser_bp.route('/books', methods=['GET', 'POST'])
def browse_books():
    books = utils.get_list_of_books()
    return render_template('books.html', book_list=books)

@browser_bp.route('/authors', methods=['GET'])
def browse_authors():
    authors = utils.get_authors()
    return render_template('authors.html', author_list=authors)


@browser_bp.route('/publishers', methods=['GET'])
def browse_publishers():
    publishers = utils.get_publishers()
    return render_template('publishers.html', publisher_list=publishers)