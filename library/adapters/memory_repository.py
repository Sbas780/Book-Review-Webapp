import csv
from pathlib import Path

from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import *
from library.adapters.jsondatareader import BooksJSONReader
import json


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__books = list()
        self.__authors = list()
        self.__users = list()
        self.__search_results = list()
        self.__publishers = list()
        self.__available_author = list()
        self.__reviews: [Review] = list()

    def get_books(self) -> list[Book]:
        return self.__books

    def add_book(self, book: Book):
        self.__books.append(book)

    def get_authors(self):
        return self.__authors

    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_number_of_books(self) -> int:
        return len(self.__books)

    def get_users(self) -> list[User]:
        return self.__users

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name):
        return next(
            (
                user
                for user in self.__users
                if user.user_name.lower() == user_name.lower()
            ),
            None,
        )

    def has_book(self, author: Author) -> bool:
        for book in self.__books:
            if author in book.authors:
                return True
        return False

    def get_search_results(self):
        return self.__search_results

    def set_search_results(self, array):
        self.__search_results = array

    def clear_search_results(self):
        self.__search_results = []

    def get_publishers(self) -> list[Publisher]:
        for book in self.__books:
            if book.publisher not in self.__publishers and book.publisher.name != "N/A":
                self.__publishers.append(book.publisher)
        return self.__publishers

    def get_available_authors(self):
        for book in self.__books:
            for author in book.authors:
                if author not in self.__available_author:
                    self.__available_author.append(author)
        return self.__available_author

    def get_book_by_id(self, book_id):
        for book in self.__books:
            if str(book.book_id) == book_id:
                return book

    def get_reviews_by_book(self, book: Book):
        results = []
        for items in self.__reviews:
            if book.book_id == items.book.book_id:
                results.append(items)
        return results

    def add_reviews(self, review_text: str, rating: int, book: Book, user_name):
        user = self.get_user(user_name)
        new_review = Review(book, review_text, rating)
        user.add_review(new_review)
        new_review.user_name = user_name
        self.__reviews.append(new_review)

    def chunks(self, data_array: [], per_page: int):
        if len(data_array) > per_page:
            for i in range(0, len(data_array), per_page):
                yield data_array[i : i + per_page]
        else:
            yield data_array

    def get_available_years(self):
        year_list = []
        for book in self.__books:
            if book.release_year and book.release_year not in year_list:
                year_list.append(book.release_year)

        return sorted(year_list)


def read_csv_file(filename: str):
    with open(filename, encoding="utf-8-sig") as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_books(data_path: Path, repo: MemoryRepository):
    authors = str(data_path / "book_authors_excerpt.json")
    comic_books = str(data_path / "comic_books_excerpt.json")
    reader_instance = BooksJSONReader(comic_books, authors)
    reader_instance.read_json_files()
    for book in reader_instance.dataset_of_books:
        repo.add_book(book)


def load_authors(data_path: Path, repo: AbstractRepository):
    authors_file = str(data_path / "book_authors_excerpt.json")
    file = open(authors_file)
    authors_file_content = file.readlines()
    for authors in authors_file_content:
        temp_dict = json.loads(authors)
        new_author = Author(int(temp_dict["author_id"]), temp_dict["name"])
        repo.add_author(new_author)


def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(user_name=data_row[1], password=generate_password_hash(data_row[2]))
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def populate(data_path: Path, repo: MemoryRepository):
    load_authors(data_path, repo)
    load_books(data_path, repo)
    load_users(data_path, repo)
