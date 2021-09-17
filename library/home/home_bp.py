from flask import Blueprint, render_template
import library.home.services as services
import library.utilities.utilities as utiles
from library.domain.model import *

home_blueprint = Blueprint('home_blueprint', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return utiles.get_list_of_books()[0].title
