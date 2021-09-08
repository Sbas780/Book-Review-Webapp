from flask import Blueprint, render_template
from library.adapters.jsondatareader import BooksJSONReader
from library.domain.model import Book, BooksInventory, Author, Review, User, Publisher
from wtforms import Form, StringField, SelectField, IntegerField, validators
from flask import flash, render_template, request, redirect

data = Blueprint('data', __name__)

books_filename = 'library/adapters/data/comic_books_excerpt.json'
authors_filename = 'library/adapters/data/book_authors_excerpt.json'
reader = BooksJSONReader(books_filename, authors_filename)
reader.read_json_files()
array = reader.dataset_of_books

@data.route('/', methods=['GET', 'POST'])
@data.route('/home', methods=['GET', 'POST'])
def home():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return find(search)
    return render_template('home.html', form=search)

def find(search):
    num = search.data['search']
    if num == "":
        flash('Enter something here')
        return redirect('home')
    else:
        results = []
        for book in array:
            if book.book_id == num:
                results.append(num)
        return results_page(array)

@data.route('/results')
def results_page(arr):
    return render_template('results.html', )

class SearchForm(Form):
    search = StringField('BookID')