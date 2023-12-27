from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import User
from backend.schemas import Message, UserList, UserPublic, UserSchema
from backend.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/create', status_code=201, response_model=UserPublic)
def create_user(new_user: UserSchema, session: Session):
    db_user = session.scalar(select(User).where(User.email == new_user.email))

    if db_user:
        raise HTTPException(status_code=400, detail='User already registered')

    user = User(
        username=new_user.username,
        email=new_user.email,
        password=get_password_hash(new_user.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get('/', response_model=UserList)
def read_users(session: Session, offset: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: Session):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@router.put('/{user_id}/update', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete('/{user_id}/delete', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'detail': 'User deleted'}
