"""File with some tests for the API."""
import pytest
import json
from flask import url_for
from tests.factory import create_transaction_id
from form3.models import Payment, PaymentMethod, Status


def test_create_valid_payment(client):
    """Test the creation of a valid payment."""
    payment_data = {
        'transaction_id': create_transaction_id(),
        'payment_method': PaymentMethod.MASTERCARD.value,
        'amount': '45.90',
        'currency': 'EUR',
    }
    response = client.post(url_for('api.create_payment'), data=json.dumps(payment_data), content_type='application/json')
    assert response.status_code == 200
    response_data = response.json
    assert response_data['id']
    assert response_data['status'] == Status.CREATED.value


@pytest.mark.parametrize("transaction_id, payment_method, amount, currency, error_message", [
    (create_transaction_id(), 'xxx', '45.90', 'EUR', {'payment_method': ['Invalid value.']}),
    (create_transaction_id(), 'VISA', '45.90', 'TTTT', {'currency': ['Length must be between 3 and 3.']}),
    (create_transaction_id(), 'VISA', 'xxxx', 'GBP', {'amount': ['Invalid value.']}),
    (None, 'VISA', 'xxxx', 'GBP', {'transaction_id': ['Field may not be null.'], 'amount': ['Invalid value.']}),

])
def test_invalid_parameters(client, transaction_id, payment_method, amount, currency, error_message):
    """Test the creation of a payment where the parameters are invalid."""
    data = {
        'transaction_id': transaction_id,
        'payment_method': payment_method,
        'amount': amount,
        'currency': currency,
    }
    response = client.post(url_for('api.create_payment'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    response_data = response.json
    assert response_data['transaction_id'] == transaction_id
    assert response_data['error_message'] == error_message


def test_missing_mandatory_parameters(client):
    """Test the creation of a payment when a mandatory attribute is missing. In this case transaction_id."""
    data = {
        'payment_method': 'VISA',
        'amount': '45.90',
        'currency': 'EUR',
    }
    response = client.post(url_for('api.create_payment'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    response_data = response.json
    assert response_data['error_message'] == {'transaction_id': ['Missing data for required field.']}


def test_create_payment_empty_request(client):
    """Test the creation of a payment where no data is provided."""
    response = client.post(url_for('api.create_payment'), data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    response_data = response.json
    assert response_data['error_message'] == 'No json request received.'


def test_get_payment(client, payment):
    """Test the retrieval of a valid payment."""
    response = client.get(url_for('api.get_payment', transaction_id=payment.transaction_id))
    assert response.status_code == 200
    response_data = response.json
    assert response_data['transaction_id'] == payment.transaction_id
    assert response_data['payment_method'] == payment.payment_method.value


def test_get_non_existent_payment(client):
    """Test if it is possible to retrieve an inexistent payment."""
    response = client.get(url_for('api.get_payment', transaction_id='11111111'))
    assert response.status_code == 404
    response_data = response.json
    assert response_data['error_message'] == 'Payment not found.'
    assert response_data['transaction_id'] == '11111111'


def test_list_payments(client, payment):
    """Test the endpoint that returns all the payments in the system."""
    response = client.get(url_for('api.list_payments'))
    assert response.status_code == 200
    response_data = response.json
    assert payment.transaction_id in [p['transaction_id'] for p in response_data['payments']]


def test_delete_payment(client, payment):
    """Test deleting a payment."""
    response = client.delete(url_for('api.delete_payment', transaction_id=payment.transaction_id))
    assert response.status_code == 200
    response_data = response.json
    assert response_data['success']


def test_delete_non_existent_payment(client):
    """Test deleting a payment that does not exist."""
    response = client.delete(url_for('api.delete_payment', transaction_id='1111111'))
    assert response.status_code == 404
    response_data = response.json
    assert response_data['error_message'] == 'Payment not found.'
    assert response_data['transaction_id'] == '1111111'


def test_update_payment(client, payment):
    """Test updating a payment."""
    new_status = Status.CHARGEBACK.value
    data = {
        'status': new_status,
    }
    assert payment.status == Status.PAID
    response = client.patch(url_for('api.update_payment', transaction_id=payment.transaction_id), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    response_data = response.json
    assert response_data['status'] == new_status

    updated_payment = Payment.query.filter_by(id=payment.id).first()
    assert updated_payment.status == new_status


def test_update_payment_invalid_parameter(client, payment):
    """Test updating a payment passing invalid parameters."""
    new_status = 'XXXX'
    data = {
        'status': new_status,
    }
    assert payment.status == Status.PAID
    response = client.patch(url_for('api.update_payment', transaction_id=payment.transaction_id), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    response_data = response.json
    assert response_data['transaction_id'] == payment.transaction_id
    assert response_data['error_message']['status'] == ['Invalid value.']

    updated_payment = Payment.query.filter_by(id=payment.id).first()
    assert updated_payment.status == Status.PAID


def test_update_non_existent_payment(client):
    """Test updating a payment that doesn't exist."""
    data = {
        'amount': '10.10',
    }
    response = client.patch(url_for('api.update_payment', transaction_id='1111111'), data=json.dumps(data),
                            content_type='application/json')
    assert response.status_code == 404
    response_data = response.json
    assert response_data['error_message'] == 'Payment not found.'
