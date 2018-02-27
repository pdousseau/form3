"""Factories used to create mock objects used in the tests."""
import factory
from random import choice
from form3.models import db, Payment, Status, PaymentMethod
from string import ascii_uppercase, digits


def create_transaction_id():
    """Create a random transaction_id with 20 characters using digits and letters.

    :return: <str> a transaction id
    """
    return ''.join(choice(ascii_uppercase + digits) for i in range(20))


class PaymentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory to create a mock payment."""

    class Meta:
        model = Payment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    transaction_id = factory.LazyFunction(create_transaction_id)
    amount = 10.50
    currency = 'EUR'
    status = Status.PAID
    payment_method = PaymentMethod.IDEAL
