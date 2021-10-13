from sqlalchemy import Table, MetaData, Column, Integer,\
    String, Date, DateTime, func, Boolean, Text, ForeignKey

from sqlalchemy.orm import mapper, relationship, synonym

from library.domain.model import *

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('pages_read', Integer)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id')),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False, server_default=func.now()),
)
authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('unique_id', Integer, primary_key=True),
    Column('full_name', String, nullable=False, unique=False),
)

books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True),
    Column('title', Text),
    Column('image', String, nullable=False),
    Column('description', String, nullable=False),
    Column('release_year', String, nullable=True),
    Column('ebook', Boolean, default=False),
    Column('image', String, nullable=False),
    Column('publisher', ForeignKey('publisher_table.id'))

)

publisher_table = Table(
    'publisher_table', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String,)
)


user_read_books = Table(
    'user_read_books', metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id'))
)

book_authors = Table(
    'book_authors', metadata,
    Column('author_id', ForeignKey('authors.id')),
    Column('book_id', ForeignKey('books.book_id')),
)


def map_model_to_tables():

    mapper(User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__pages_read': users_table.c.pages_read
    })

    mapper(Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__image': books_table.c.image,
        '_Book__release_year': books_table.c.release_year,
        '_Book__description': books_table.c.description,
        '_Book__ebook': books_table.c.ebook,
        '_authors': relationship(Author, secondary=book_authors),
        '_publisher': relationship(Publisher)
    })


    mapper(Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.unique_id,
        '_Author__full_name': authors_table.c.full_name
    })

    mapper(Publisher, publisher_table, properties={
        '_name': publisher_table.c.name
    })




