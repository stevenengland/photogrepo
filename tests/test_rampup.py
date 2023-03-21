import tests
import app
import pytest

from django.contrib.auth.models import User

def test_example():
    print('run test')
    assert 1==1

@pytest.mark.django_db
def test_user_creation():
    User.objects.create_user('test', 'test@example.com', 'test')
    assert User.objects.count() == 1
