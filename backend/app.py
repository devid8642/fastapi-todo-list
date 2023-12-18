from fastapi import FastAPI

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
