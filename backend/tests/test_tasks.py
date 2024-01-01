import factory.fuzzy

from backend.models import Task, TodoState


class TaskFactory(factory.Factory):
    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1

    class Meta:
        model = Task


def test_create_task(client, token):
    response = client.post(
        '/tasks/create/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test',
            'description': 'Test',
            'state': 'draft',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'title': 'Test',
        'description': 'Test',
        'state': 'draft',
    }


def test_get_tasks(session, user, client, token):
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/tasks/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert len(response.json()['tasks']) == 5


def test_get_tasks_with_pagination(session, user, client, token):
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))

    response = client.get(
        '/tasks/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['tasks']) == 2


def test_get_tasks_with_title(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, title='Test title 1')
    )
    session.commit()

    response = client.get(
        '/tasks/?title=Test title 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['tasks']) == 5


def test_get_tasks_with_description(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5, user_id=user.id, description='Test description 1'
        )
    )
    session.commit()

    response = client.get(
        '/tasks/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['tasks']) == 5


def test_get_tasks_with_state(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        '/tasks/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['tasks']) == 5


def test_get_tasks_with_filter_combined(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5,
            title='Test title',
            description='Test decription',
            state=TodoState.todo,
            user_id=user.id,
        )
    )

    session.bulk_save_objects(
        TaskFactory.create_batch(
            3,
            title='Other title',
            description='Other description',
            state=TodoState.done,
            user_id=user.id,
        )
    )

    session.commit()

    response = client.get(
        '/tasks/?title=Test&description=Test&state=todo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert len(response.json()['tasks']) == 5


def test_update_task(client, session, user, token):
    task = TaskFactory(user_id=user.id)

    session.add(task)
    session.commit()

    response = client.post(
        f'/tasks/{task.id}/update/',  # type: ignore
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'new title'},
    )

    assert response.status_code == 200
    assert response.json()['title'] == 'new title'


def test_update_not_existing_task(client, token):
    response = client.post(
        '/tasks/10/update/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'new title'},
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found.'


def test_delete_task(client, session, user, token):
    task = TaskFactory(user_id=user.id)

    session.add(task)
    session.commit()

    response = client.delete(
        f'/tasks/{task.id}/delete/',  # type: ignore
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json()['detail'] == 'Task has been deleted successfully.'


def test_delete_not_existing_task(client, token):
    response = client.delete(
        '/tasks/10/delete/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Task not found.'
