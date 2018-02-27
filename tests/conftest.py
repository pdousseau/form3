import pytest
from pytest_factoryboy import register
from tests.factory import PaymentFactory
from form3 import create_app

register(PaymentFactory)


@pytest.fixture
def app():
    return create_app()
