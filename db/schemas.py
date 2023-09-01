from typing import Optional
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

class PropertyBase(BaseModel):
    address: str
    class_description: str
    bldg_use: str | None
    estimated_market_value: int | None
    bldg_sq_ft: int | None

class Property(PropertyBase):
    id: int

    class Config:
        orm_mode = True

class UserProperty(BaseModel):
    property_id: int
