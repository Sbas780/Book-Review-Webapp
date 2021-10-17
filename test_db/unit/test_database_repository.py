from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.authentication import services
from library.domain.model import Publisher, Author, Book, Review, User
from library.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('ben', 'Password12345')
    repo.add_user(user)

    assert repo.get_user('ben') is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user("fmercury")

    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')

    assert user is None

def test_repository_can_get_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books = repo.get_books()

    assert len(books) == 20


def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    new_book = Book(45, "Test Book Four")
    repo.add_book(new_book)
    book = repo.get_book_by_id(45)

    assert book == new_book

def test_repository_add_duplicate_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = Book(1, "Test Book One")
    new_book = Book(2, "Test Book Two")
    repo.add_book(book)
    repo.add_book(new_book)
    books = repo.get_books()

    assert books == [Book(1, "Test Book One"), Book(2, "Test Book Two"), Book(3, "Test Book Three")]

def test_repository_can_get_book_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book_by_id(1)

    assert book == Book(1, "Test Book One")

def test_repository_cannot_get_book_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book_by_id(6)

    assert book is None

# def test_repository_author_has_a_book(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#     status = repo.has_book(Author(1, "Test Author"))
#
#     assert status is True

# def test_repository_author_has_no_book(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
#     status = repo.has_book(Author(7, "Test Author Seven"))
#     assert status is False

def test_repository_get_number_of_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    length = repo.get_number_of_books()

    assert length == 20


def test_repository_can_get_available_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    authors = repo.get_available_authors()
    authors_count = len(authors)

    assert authors_count == 31


def test_repository_get_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publishers = repo.get_publishers()
    assert publishers == [Publisher("Publisher One"), Publisher("Publisher Two"), Publisher("Publisher Three")]

def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book_by_id(13340336)

    # Check that the Book has the expected tit
    # le.
    assert book.title == '20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)'

    # Check that the Book is reviewed as expected.


def test_repository_does_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book_by_id(321)

    assert book is None


def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_author = Author(123, "test_author")
    repo.add_author(test_author)

    assert test_author in repo.get_authors()


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_book = repo.get_book_by_id(27036536)
    test_review = Review(test_book, "Cool book!", 5)
    repo.add_review(test_review)

    assert test_review == repo.get_reviews_by_book(test_book)[-1]


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_reviews()) == 1

def test_repository_get_available_years(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    years = repo.get_available_years() #Should return all available years ignoring NULL types and duplicates
    assert len(years) == 8

def test_repository_chunks(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    chunks = repo.chunks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 5)
    assert list(chunks) == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12]]