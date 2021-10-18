import pytest

from library.authentication import services as services
from library.authentication.services import NameNotUniqueException, AuthenticationException
from library.adapters.database_repository import SqlAlchemyRepository

def test_add_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    username = 'abc123'
    password = 'abcABC123'

    services.add_user(username, password, repo)
    user = services.get_user(username, repo)
    user_as_dict = services.get_user(username, repo)

    assert user_as_dict['user_name'] == username

    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(NameNotUniqueException):
        services.add_user(user_name, password, repo)


def test_authentication_with_valid_credentials(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, repo)

    try:
        services.authenticate_user(new_user_name, new_password, repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    services.add_user(new_user_name, new_password, repo)

    with pytest.raises(services.AuthenticationException):
        services.authenticate_user(new_user_name, '0987654321', repo)

