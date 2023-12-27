from fastapi import FastAPI
from backend.routers import auth, users

app = FastAPI(title='My Study App')
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def home():
    return {'message': 'Olá Mundo!'}
