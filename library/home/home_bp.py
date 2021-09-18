from flask import Blueprint, render_template
import library.utilities.utilities as utils
from library.search.search import SearchForm, request

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/', methods=['GET'])
@home_blueprint.route('/home', methods=['GET'])
def home():
    form = SearchForm(request.args, meta={'csrf': False})
    book_list = utils.get_list_of_books()

    return render_template('home.html',
                           form=form)

