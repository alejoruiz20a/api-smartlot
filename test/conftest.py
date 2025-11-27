import pytest
from app import create_app, db
from flask_jwt_extended import create_access_token
from app.models import User

@pytest.fixture
def app():
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_token(app):
    user = User(full_name='Test User', email='test@example.com')
    user.set_password('1234')
    db.session.add(user)
    db.session.commit()
    return create_access_token(identity=user.id)