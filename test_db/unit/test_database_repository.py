from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.authentication import services
from library.domain.model import Publisher, Author, Book, Review, User
from library.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('test_user', '123456789')
    repo.add_user(user)
    repo.add_user(User('test_user2', '123456789'))
    user2 = repo.get_user('test_user')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('unaruto')

    assert user == User('unaruto', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('hkakashi')

    assert user is None


def test_repository_can_retrieve_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_books = repo.get_number_of_books()

    assert number_of_books == 20


def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_books = repo.get_number_of_books()
    test_book = Book(123, 'test_book')
    repo.add_book(test_book)

    assert repo.get_book_by_id(123) == test_book


def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book_by_id(13340336)

    # Check that the Book has the expected title.
    assert book.title == '20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)'

    # Check that the Book is reviewed as expected.


def test_repository_does_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    article = repo.get_book_by_id(321)

    assert article is None


def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_author = Author(123, "test_author")
    repo.add_author(test_author)

    assert test_author in repo.get_authors()


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_book = repo.get_book_by_id(13340336)
    user = User('test_user', '123456789')
    test_review = Review(test_book, "Cool book!", 5, user)
    repo.add_review(13340336, test_review)

    for book_dictionary in repo.get_reviews():
        if book_dictionary['book_id'] == 13340336:
            assert test_review in book_dictionary['reviews']


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 20
