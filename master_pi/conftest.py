import os
import tempfile

import pytest
from app import create_app, get_db
from socket_server.server import Server

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

    yield app

    # Dropping database
    with app.app_context():
        get_db().drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def socket():
    server = Server()
    server.start_socket_server()

    yield server

    server.stop_socket_server()
