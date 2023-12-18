from fastapi import FastAPI, HTTPException

from .schemas import User, UserDB, UserList, UserPublic

app = FastAPI()
database = []


@app.get('/')
async def home():
    return {'message': 'Olá Mundo!'}


@app.post('/users/create/', status_code=201, response_model=UserPublic)
async def create_user(user: User):
    user = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user)

    return user


@app.get('/users/', response_model=UserList)
async def get_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=UserPublic)
async def get_user(user_id: int):
    if user_id > len(database) or user_id < 0:
        raise HTTPException(status_code=404, detail='User not found')
    return database[user_id - 1]
