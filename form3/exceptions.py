from flask import jsonify


class Form3Exception(Exception):
    def __init__(self, message, transaction_id, status_code):
        Exception.__init__(self)
        self.message = message
        self.transaction_id = transaction_id
        self.status_code = status_code


class InvalidRequest(Form3Exception):
    """Exception used when a request is malformed, either because there are mandatory fields missing or because their
    value is incorrect."""
    def __init__(self, message, transaction_id=None):
        Form3Exception.__init__(self, message, transaction_id, 400)


class ResourceNotFound(Form3Exception):
    """Exception used when a payment or other object could not be found."""
    def __init__(self, message, transaction_id=None):
        Form3Exception.__init__(self, message, transaction_id, 404)


def exception_handler(exception):
    """Exception handler used to convert Form3Exceptions to a json response.

    :param exception: <Form3Exception> the exception raised
    :return: <json> a json response that contains the error details
    """
    resp = jsonify({'error_message': exception.message, 'transaction_id': exception.transaction_id})
    resp.status_code = exception.status_code
    return resp
