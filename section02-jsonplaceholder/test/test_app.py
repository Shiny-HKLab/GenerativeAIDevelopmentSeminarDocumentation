# from app import get_user
from solution.app import get_user

def test_get_user():
    user = get_user(1)
    assert user is not None
    assert user['id'] == 1
    assert user['name'] is not None
    assert user['email'] is not None

def get_posts_by_user():
    pass

