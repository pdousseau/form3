from form3 import create_app, db


def create_db():
    db.create_all()

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        create_db()
