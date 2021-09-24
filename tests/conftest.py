import pytest
import warnings
from library import create_app
from utils import get_project_root
from library.adapters import memory_repository
from library.adapters.memory_repository import MemoryRepository
TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture()
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture()
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
    })
    return my_app.test_client()


class AuthenticationManager():
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='thorke', password='cLQ^C#oFXlo'):
        return self.__client.post('authentication/login', data={'user_name': user_name, 'password': password})

    def logout(self):
        return self.__client.get('/auth/logout')

@pytest.fixture()
def auth(client):

    return AuthenticationManager(client)