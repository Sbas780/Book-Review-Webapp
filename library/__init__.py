"""Initialize Flask app."""

from flask import Flask, render_template

import config
from library.blueprints.data_blueprint import data


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.register_blueprint(data)
    return app