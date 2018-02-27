from flask import Flask
from form3.app import api
from form3.exceptions import exception_handler, Form3Exception
from form3.models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form3.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(api)
    app.register_error_handler(Form3Exception, exception_handler)
    db.init_app(app)
    return app
