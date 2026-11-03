import pytest
from app import create_app, db
from app.models import User, Note

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_create_user(client):
    response = client.post('/users', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'

def test_create_and_get_notes(client):
    user_res = client.post('/users', json={'username': 'author', 'email': 'author@example.com'})
    user_id = user_res.get_json()['id']

    note_res = client.post('/notes', json={
        'title': 'Test Note',
        'content': 'Hello World',
        'category': 'work',
        'user_id': user_id
    })
    assert note_res.status_code == 201

    get_res = client.get('/notes?category=work')
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert data['total'] == 1
    assert data['notes'][0]['title'] == 'Test Note'
