from sqlalchemy import select

from backend.models import Task, User


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


def test_create_task(session, user):
    task = Task(
        title='Test',
        description='Test',
        state='draft',
        user_id=user.id,
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    user = session.scalar(select(User).where(User.id == user.id))

    assert task in user.tasks
