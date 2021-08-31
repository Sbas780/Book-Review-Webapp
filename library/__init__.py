"""Initialize Flask app."""

from flask import Flask, render_template
from library.adapters.data_blueprint import data


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('layout.html')
    app.register_blueprint(data)
    return app