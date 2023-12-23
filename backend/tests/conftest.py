import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import app
from backend.database import get_session
from backend.models import Base, User
from backend.security import get_password_hash


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)

    yield Session()

    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    password = 'secret'
    new_user = User(
        username='devid',
        email='devid@example.com',
        password=get_password_hash(password),
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    new_user.plain_password = password  # type: ignore

    return new_user
