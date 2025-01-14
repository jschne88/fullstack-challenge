from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
