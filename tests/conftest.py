import pytest
from app import app as flask_app
from flask import url_for


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
