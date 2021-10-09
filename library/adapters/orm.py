from sqlalchemy import Table, MetaData, Column, Integer,\
    String, Date, DateTime, func, Boolean, Text, ForeignKey

from sqlalchemy.orm import mapper, relationship, synonym

from library.domain.model import *

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('pages_read', Integer, nullable=False, server_default="0")
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id')),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False, server_default=func.now()),
)

books = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True),
    Column('title', Text),
    Column('image', String, nullable=False),
    Column('publisher', ForeignKey('publishers.publisher_id')),
    Column('release_year', String, nullable=True),
    Column('ebook', Boolean, default=False),
    Column('image', String, nullable=False),
    Column('description', Text)
)

authors = Table(
    'authors', metadata,
    Column('unique_id', Integer, primary_key=True),
    Column('full_name', String, nullable=False, unique=True),
)

publishers = Table(
    'publishers', metadata,
    Column('publisher_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False)
)

user_read_books = Table(
    'user_read_books', metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('book_id', ForeignKey('books.book_id'), primary_key=True)
)

book_authors = Table(
    'book_authors', metadata,
    Column('book_id', ForeignKey('books.book_id'), primary_key=True),
    Column('author_id', ForeignKey('authors.unique_id'), primary_key=True)
)

def map_model_to_tables():

    mapper(User, users, properties={
        '_User_user_name': users.c.user_name,
        '_User_password': users.c.password,
        '_User_pages_read': users.c.pages_read,
        '_User_read_books': relationship(Book, secondary=user_read_books)
    })

    mapper(Book, books, properties={
        '_Books_book_id': books.c.book_id,
        '_Books_title': books.c.title,
        '_Books_image': books.c.image,
        '_Books_release_year': books.c.release_year,
        '_Books_description': books.c.description,
        '_Books_ebook': books.c.ebook,
        '_Books_publisher': relationship(Publisher),
        '_Books_authors': relationship(Author, secondary=book_authors),

    })

    mapper(Publisher, publishers, properties={
        '_Publisher_name': publishers.c.name
    })

    mapper(Author, authors, properties={
        '_Author_unique_id': authors.c.unique_id,
        '_Author_full_name': authors.c.full_name
    })




