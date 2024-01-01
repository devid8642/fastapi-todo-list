from pydantic import BaseModel, ConfigDict, EmailStr

from backend.models import TodoState


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class TaskSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TaskPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
