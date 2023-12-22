from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_session
from .models import User
from .schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI(title='My Study App')
database = []


@app.get('/')
async def home():
    return {'message': 'Olá Mundo!'}


@app.post('/users/create/', status_code=201, response_model=UserPublic)
def create_user(new_user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.email == new_user.email))

    if db_user:
        raise HTTPException(status_code=400, detail='User already registered')

    user = User(
        username=new_user.username,
        email=new_user.email,
        password=new_user.password,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.get('/users/', response_model=UserList)
def read_users(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 100
):
    users = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': users}


@app.get('/users/{user_id}/', response_model=UserPublic)
async def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@app.put('/users/{user_id}/update/', response_model=UserPublic)
async def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}/delete/', response_model=Message)
async def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    del database[user_id - 1]

    return {'detail': 'User deleted'}
