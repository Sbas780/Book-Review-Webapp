import pytest
import warnings
from library.search import services as services
from library.authentication.services import NameNotUniqueException, AuthenticationException
from library.adapters.database_repository import SqlAlchemyRepository

def test_search_with_empty_string(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = []
    publishers = []
    years = []
    ebook = None
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 20

def test_search_with_specific_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = ["Garth Ennis"]
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 2


def test_search_with_non_existent_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = ["False Author"]
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 0

def test_search_with_multiple_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = ["Test Author", "Test AuthorTwo"]
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 0

def test_search_with_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = []
    years = []
    ebook = None
    publishers = ["Planeta DeAgostini", "Dargaud"]
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 2


def test_search_with_non_existent_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = []
    years = []
    ebook = None
    publishers = ["Publisher Five"]
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 0


def test_search_with_years(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = []
    years = [2012, 1997]
    ebook = None
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 4

def test_search_with_invalid_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = []
    years = [2021, 2022]
    ebook = None
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 0


def test_search_with_mixed_years(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = []
    years = [2021, 2016]
    ebook = None
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 5


def test_search_for_query(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = "Two"
    authors = []
    years = []
    ebook = None
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 1


def test_search_for_query_and_search_params(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = "Two"
    authors = ["False Author"]
    years = [2021]
    ebook = None
    publishers = ["Publisher Two"]
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 0

def test_search_for_ebook_false(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    query = ""
    authors = []
    years = []
    ebook = "False"
    publishers = []
    results = services.search_for_items(repo, query, authors, publishers, years, ebook)
    assert len(results) == 16
