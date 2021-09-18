from flask import Blueprint, render_template
import library.utilities.utilities as utils
from library.search.search import SearchForm, request

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    form = SearchForm(request.args, meta={'csrf': False})
    book_list = utils.get_list_of_books()

    return render_template('home.html', book_list=book_list, number_of_books=utils.get_number_of_books(), form=form)
