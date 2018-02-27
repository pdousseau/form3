"""File that defines all the schema used in the system to serialize and deserialize responses and requests. On thing
that would be nice to do here is to create custom error messages."""
from decimal import Decimal, InvalidOperation
from enum import Enum

from marshmallow import Schema, post_load, validate
from marshmallow.fields import Str, Integer, Function, List, Nested
from form3.models import Payment, Status, PaymentMethod

# dump = response/serialize, load = request


def is_decimal(amount):
    """Method that checks if a number is convertible to decimal."""
    try:
        Decimal(amount)
        return True
    except InvalidOperation:
        return False


class PaymentSchema(Schema):
    """Schema used to serialize and deserialize payment objects."""
    id = Integer(dump_only=True)
    transaction_id = Str(required=True)
    amount = Str(required=True, validate=is_decimal)
    currency = Str(required=True, validate=validate.Length(min=3, max=3))  # validate the size of the currency
    status = Function(serialize=lambda p: p.status.value if isinstance(p.status, Enum) else p.status,
                      validate=lambda x: hasattr(Status, x))  # return only the value of the status
    # validate whether it is a valid payment method
    payment_method = Function(serialize=lambda x: x.payment_method.value, required=True,
                              validate=lambda x: hasattr(PaymentMethod, x))

    @post_load
    def make_payment(self, data):
        return Payment(**data, status=Status.CREATED)


class ListPaymentSchema(Schema):
    """Schema used to return a list of payments."""
    payments = List(Nested(PaymentSchema))
