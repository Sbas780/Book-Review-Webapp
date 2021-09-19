from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

import library.utilities.utilities as utils
import library.adapters.repository as repo


browser_bp = Blueprint('browser_bp', __name__, url_prefix='/browsing')

@browser_bp.route('/books', methods=['GET', 'POST'])
def browse_books():
    form = SortField(request.args, meta={'csrf': False})
    books = utils.get_list_of_books()
    select = request.args.get('sort')
    if select == "New":
        return "Yes"
    return render_template('books.html', book_list=books, form=form)

@browser_bp.route('/authors', methods=['GET'])
def browse_authors():
    authors = utils.get_authors()
    return render_template('authors.html', author_list=authors)

@browser_bp.route('/something')
def browse_something():
    return "BROOOO"


class SortField(FlaskForm):
    sort = SelectField("Sort by: ", choices=[(1, "Default"), (2, "New"), (3, "Old"), (4, "Rating")], default=1)
    submit = SubmitField('submit')
