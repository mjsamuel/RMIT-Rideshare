import os, pytest, sys
sys.path.append('./socket_server/')

from app import create_app, get_db

with open(os.path.join(os.path.dirname(__file__), 'tests', 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True
    })

    # Populating database with entries from /tests/data.sql
    with app.app_context():
        db = get_db()
        db.session.execute(_data_sql)
        db.session.commit()

    return app

@pytest.fixture
def client(app):
    return app.test_client()
