from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import User
from backend.schemas import Message, Token, UserList, UserPublic, UserSchema
from backend.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)

app = FastAPI(title='My Study App')


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
        password=get_password_hash(new_user.password),
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
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user


@app.put('/users/{user_id}/update/', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}/delete/', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    session.delete(db_user)
    session.commit()

    return {'detail': 'User deleted'}


@app.post('/token/', response_model=Token)
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    acess_token = create_access_token(data={'user_email': user.email})

    return {'acess_token': acess_token, 'token_type': 'bearer'}
