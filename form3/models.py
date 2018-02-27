"""File that contains all the models used by the application."""
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Status(Enum):
    PAID = 'PAID'
    CHARGEBACK = 'CHARGEBACK'
    REFUSED = 'REFUSED'
    ERROR = 'ERROR'
    PENDING = 'PENDING'
    REFUNDED = 'REFUNDED'
    CREATED = 'CREATED'


class PaymentMethod(Enum):
    VISA = 'VISA'
    MASTERCARD = 'MASTERCARD'
    IDEAL = 'IDEAL'
    PAYPAL = 'PAYPAL'
    GIROPAY = 'GIROPAY'


class Payment(db.Model):
    """Table with payments."""
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(120), unique=True, nullable=False)  # payment reference
    # OBS: I used String here because SQLite does not support decimal natively, and I used Sqlite because I wanted
    # something that would work out of the box for this assignment. If this would be a production code, I would
    # certainly use something like MySQL or PostgreSQL and set this field to something like:
    # db.Numeric(precision='10,4'). Another possibility would be to store this field in its lowest denomination so
    # 10.918 would be converted to 10918 and it would be possible to use an integer field.
    amount = db.Column(db.String(20), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethod), nullable=False)
