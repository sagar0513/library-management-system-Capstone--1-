import pytest
from app import app, db, User, Book

# Fixture for setting up the test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    with app.app_context():
        db.drop_all()

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302  # Redirect to login
    assert response.headers['Location'] == '/login'  # Check for relative URL

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_success(client):
    with app.app_context():
        user = User(username='admin')
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={'username': 'admin', 'password': 'password'})
    assert response.status_code == 302  # Redirect to book_management

def test_login_failure(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert b'Login failed' in response.data

def test_book_management_page(client):
    with app.app_context():
        user = User(username='admin')
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={'username': 'admin', 'password': 'password'})
    assert response.status_code == 302  # Ensure login success

    response = client.get('/book_management')
    assert response.status_code == 200  # Now it should be accessible

def test_cart_page(client):
    with app.app_context():
        user = User(username='admin')
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={'username': 'admin', 'password': 'password'})
    assert response.status_code == 302  # Ensure login success

    response = client.get('/cart')
    assert response.status_code == 200  # Now it should be accessible
    
