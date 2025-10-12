from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    email: EmailStr
    login: str = Field(..., min_length=3, max_length=30)
    password: str
    createdAt: datetime
    updatedAt: datetime


class UserCreate(BaseModel):
    email: EmailStr
    login: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    login: Optional[str] = Field(None, min_length=3, max_length=30)
    password: Optional[str] = Field(None, min_length=6)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    login: str
    createdAt: datetime
    updatedAt: datetime


class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    authorId: int


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class PostOut(PostBase):
    id: int
    authorId: int
    createdAt: datetime
    updatedAt: datetime
