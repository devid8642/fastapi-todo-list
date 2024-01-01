from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import Task, User
from backend.schemas import (
    Message,
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
from backend.security import get_current_user

router = APIRouter(prefix='/tasks', tags=['tasks'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/create', status_code=201, response_model=TaskPublic)
def create_task(task: TaskSchema, user: CurrentUser, session: Session):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=user.id,
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get('/', response_model=TaskList)
def get_tasks(
    session: Session,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = 0,
    limit: int = 100,
):
    query = select(Task).where(Task.user_id == user.id)

    if title:
        query = query.filter(Task.title.contains(title))  # type: ignore

    if description:
        query = query.filter(  # type: ignore
            Task.description.contains(description)
        )

    if state:
        query = query.filter(Task.state == state)  # type: ignore

    tasks = session.scalars(  # type: ignore
        query.offset(offset).limit(limit)  # type: ignore
    ).all()

    return {'tasks': tasks}


@router.post('/{task_id}/update/', response_model=TaskPublic)
def update_task(
    task_id: int, session: Session, user: CurrentUser, task: TaskUpdate
):
    task_db = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task_db:
        raise HTTPException(status_code=404, detail='Task not found.')

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(task_db, key, value)

    session.add(task_db)
    session.commit()
    session.refresh(task_db)

    return task_db


@router.delete('/{task_id}/delete/', response_model=Message)
def delete_task(task_id: int, session: Session, user: CurrentUser):
    task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task:
        raise HTTPException(status_code=404, detail='Task not found.')

    session.delete(task)
    session.commit()

    return {'detail': 'Task has been deleted successfully.'}
