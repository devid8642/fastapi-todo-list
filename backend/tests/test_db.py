from sqlalchemy import select

from backend.models import User


def test_create_user(session):
    new_user = User(
        username='devid', email='devid@devid.com', password='secret'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.id == 1))

    assert user.username == 'devid'
    assert user.email == 'devid@devid.com'
    assert user.password == 'secret'
