from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm  import sessionmaker
from database import Base
from main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from models import Todos, Users
from routers.auth import bcrypt_context

SQL_ALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL,connect_args={"check_same_thread" : False},poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {
        'username': 'ksikora@test.com',
        'id': 1,
        'role': 'admin'
    }

client = TestClient(app)

attrs = {
    'title': "Lear to code",
    'description':  "so that you are a better manager :)",
    'priority' : 5,
    'owner_id': 1
}

@pytest.fixture
def test_todo():
    todo = Todos(**attrs)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as conn:
        conn.execute(text("DELETE from todos"))
        conn.commit()

@pytest.fixture
def test_user():
    user = Users(
        username = 'sikora',
        email = 'sikora@gmail.com',
        first_name = 'Kris',
        last_name = 'Sikora',
        hashed_password = bcrypt_context.hash('onyx'),
        role = 'admin',
        phone_number = '111-111-111'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with engine.connect() as conn:
        conn.execute(text("DELETE from users"))
        conn.commit()
