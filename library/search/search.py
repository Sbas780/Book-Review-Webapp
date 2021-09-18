from flask import Blueprint, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import library.utilities.utilities as utils
from .services import search_for_items
import library.adapters.repository as repo

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.args, meta={'cgsrf': False})
    if search == 'POST':
        redirect('search')
    # query = request.args.get('search', '')
    # results = search_for_items(query)
    return render_template('search.html', form=form)



class SearchForm(FlaskForm):
    search = StringField('search')
    submit = SubmitField('submit')
