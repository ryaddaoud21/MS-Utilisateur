import pytest
from flask import Flask
from API.auth import auth_blueprint
from API.models import db, User


@pytest.fixture
def app():
    app = Flask(__name__)

    # Utiliser une base de données SQLite en mémoire pour les tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Enregistrement du blueprint auth
    app.register_blueprint(auth_blueprint, url_prefix='/')

    with app.app_context():
        db.create_all()

        # Ajouter des utilisateurs fictifs pour les tests
        admin_user = User(username='admin', password='password', role='admin')
        user1 = User(username='user1', password='userpass', role='user')
        db.session.add_all([admin_user, user1])
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_login(client):
    response = client.post('/login', json={'username': 'admin', 'password': 'password'})
    assert response.status_code == 200
    assert 'token' in response.json


def test_login_fail(client):
    response = client.post('/login', json={'username': 'admin', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.json['msg'] == 'Invalid credentials'


def test_token_required(client):
    response = client.get('/protected', headers={})  # No token provided
    assert response.status_code == 401
    assert response.json['error'] == 'Unauthorized'



def test_missing_credentials(client):
    response = client.post('/login', json={})
    assert response.status_code == 400
    assert response.json['msg'] == 'Username and password required'


def test_logout(client):
    # Connexion pour obtenir un token
    login_response = client.post('/login', json={'username': 'admin', 'password': 'password'})
    token = login_response.json['token']

    # En-tête d'autorisation avec le token
    headers = {'Authorization': f'Bearer {token}'}

    # Déconnexion
    logout_response = client.post('/logout', headers=headers)

    assert logout_response.status_code == 200
    assert logout_response.json['msg'] == 'Successfully logged out'


def test_logout_without_token(client):
    logout_response = client.post('/logout')
    assert logout_response.status_code == 401
    assert logout_response.json['error'] == 'Unauthorized'


