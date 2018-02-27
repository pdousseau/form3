"""API that allows to create, update and delete a payment, and also to retrieve a list with all the payments in the
system.
"""
import json
from flask import request, Blueprint
from form3.models import db, Payment
from serialization import PaymentSchema, ListPaymentSchema
from form3.exceptions import InvalidRequest, ResourceNotFound

api = Blueprint('api', __name__, url_prefix='/')


@api.route('payment/<string:transaction_id>', methods=['GET'])
def get_payment(transaction_id):
    """Endpoint used to retrieve a payment.

    :param transaction_id: <str> the transaction id of the payment
    :return: <json> the payment information
    :except ResourceNotFound: exception raised in case the payment is not found
    """
    payment = Payment.query.filter_by(transaction_id=transaction_id).first()

    if not payment:
        raise ResourceNotFound('Payment not found.', transaction_id=transaction_id)

    return PaymentSchema().dumps(payment)


@api.route('payment', methods=['POST'])
def create_payment():
    """Endpoint used to create a new payment.

    :return: <json> details about the payment just created
    :exception InvalidRequest: raised in case the request is invalid.
    """
    data = request.get_json()

    # in case no json data was supplied
    if not data:
        raise InvalidRequest('No json request received.')

    # load the schema and validate if all the fields are correct
    payment, errors = PaymentSchema().load(data)

    # in case an attribute was invalid (for instance an invalid payment method name)
    if errors:
        raise InvalidRequest(errors, transaction_id=data.get('transaction_id'))

    # add the payment to the session and commit
    db.session.add(payment)
    db.session.commit()
    return PaymentSchema().dumps(payment)


@api.route('payment/<string:transaction_id>', methods=['DELETE'])
def delete_payment(transaction_id):
    """Endpoint used to delete a payment.

    :param transaction_id: <str> transaction id of the payment being updated
    :return: <json> all the fields of the updated payment
    """
    payment = Payment.query.filter_by(transaction_id=transaction_id).first()

    if not payment:
        raise ResourceNotFound('Payment not found.', transaction_id=transaction_id)

    db.session.delete(payment)

    return json.dumps({'success': True}), 200, {'ContentType':  'application/json'}


@api.route('payment/<string:transaction_id>', methods=['PATCH'])
def update_payment(transaction_id):
    """Endpoint used to update a set of field of a payment.

    :param transaction_id: <str> the transaction id of the payment
    :return: <json> the fields of the update payment
    """

    data = request.json
    if not data:
        raise InvalidRequest('No json request received.')

    payment, errors = PaymentSchema().load(data)

    # check if any of the errors listed is related to the fields being updated. To avoid this it would also be possible
    # to create a schema just for update the payment, so the other fields wouldn't be mandatory.
    has_errors = list(filter(lambda x: x in data, errors))

    if has_errors:

        # retrieve the relevant errors
        filtered_errors = {key: errors[key] for key in has_errors}
        raise InvalidRequest(filtered_errors, transaction_id=transaction_id)

    original_payment = Payment.query.filter_by(transaction_id=transaction_id).first()

    if not original_payment:
        raise ResourceNotFound('Payment not found.', transaction_id=transaction_id)

    for key, value in data.items():
        setattr(original_payment, key, value)

    return PaymentSchema().dumps(original_payment)


@api.route('payment', methods=['GET'])
def list_payments():
    """Endpoint that lists all the payments in the system.

    :return: <json> a json response with a list of payments.
    """
    payments = Payment.query.all()
    return ListPaymentSchema().dumps({'payments': payments})
