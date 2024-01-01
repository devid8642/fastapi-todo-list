from fastapi import FastAPI

from backend.routers import auth, tasks, users

app = FastAPI(title='My Study App')
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get('/')
async def home():
    return {'message': 'Olá Mundo!'}
