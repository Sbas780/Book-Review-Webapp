from flask import Blueprint, render_template
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Book, BooksInventory, Author, Review, User, Publisher

data = Blueprint('data', __name__)

books_filename = 'library/adapters/data/comic_books_excerpt.json'
authors_filename = 'library/adapters/data/book_authors_excerpt.json'
reader = BooksJSONReader(books_filename, authors_filename)
reader.read_json_files()
array = reader.dataset_of_books

@data.route('/', methods=["GET"])
def home():
    return render_template('home.html', array=array)
