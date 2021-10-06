"""Initialize Flask app."""
from pathlib import Path
from flask import Flask
import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool
from library.adapters.orm import metadata, map_model_to_tables
from library.adapters import memory_repository, database_repository, repository_populate

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
        database_uri = app.config["SQLALCHMY_DATABASE_URI"]
        database_echo = app.config["SQLALCHEMY_ECHO"]

        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            repository_populate.populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

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

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app