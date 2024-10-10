import warnings
import pytest
from app import app, db_session, ChatHistory  # Adjust the import based on your app structure

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def suppress_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'ChatGPT-like Flask App' in response.data
