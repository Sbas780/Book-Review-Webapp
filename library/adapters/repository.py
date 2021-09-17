import abc
from typing import List
from datetime import date

from library.domain.model import *

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_books(self) -> list[Book]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        raise NotImplementedError