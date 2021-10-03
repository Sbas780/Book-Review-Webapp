"""Initialize Flask app."""
from pathlib import Path
from flask import Flask
import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_object("config.Config")

    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']



    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = MemoryRepository()
        populate(data_path, repo.repo_instance)

    if app.config['REPOSITORY'] == 'database':
        repo.repo_instance = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

    with app.app_context():
        from .home import home_bp
        app.register_blueprint(home_bp.home_blueprint)

        from .search import search
        app.register_blueprint(search.search_bp)

        from .browser import browser_bp
        app.register_blueprint(browser_bp.browser_bp)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .user import user_bp
        app.register_blueprint(user_bp.user_blueprint)

    return app