"""Initialize Flask app."""
from pathlib import Path
from flask import Flask
import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_object("config.Config")

    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        from .home import home_bp
        app.register_blueprint(home_bp.home_blueprint)

        from .search import search
        app.register_blueprint(search.search_bp)

    return app