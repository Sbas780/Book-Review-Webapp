from flask import Blueprint, render_template
import library.utilities.utilities as utils
import library.adapters.repository as repo


browser_bp = Blueprint('browser_bp', __name__, url_prefix='/browsing')

@browser_bp.route('/books', methods=['GET'])
def browse_books():
    books = utils.get_list_of_books()
    return render_template('books.html', book_list=books)

@browser_bp.route('/authors', methods=['GET'])
def browse_authors():
    authors = utils.get_authors()
    return render_template('authors.html', author_list=authors)