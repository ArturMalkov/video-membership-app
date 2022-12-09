import pytest

from app import db
from app.users.models import User


@pytest.fixture(scope="module")
def setup():
    # setup
    session = db.get_session()
    yield session
    # teardown
    query = User.objects.filter(email="test@test.com")
    if query.count() != 0:
        query.delete()
    session.shutdown()


def test_create_user(setup):
    User.create_user(email="test@test.com", password="abc123")


def test_duplicate_user(setup):
    with pytest.raises(Exception):
        User.create_user(email="test@test.com", password="abc123")


def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email="test@test", password="abc123")


def test_valid_password(setup):
    query = User.objects.filter(email="test@test.com")
    assert query.count() == 1
    user = query.first()
    assert user.verify_password("abc123") is True
    assert user.verify_password("abc1234") is False
