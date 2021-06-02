from typing import List, Optional
from datetime import date
from pydantic import BaseModel, EmailStr

#########################################
#                                       #
#                 Posts                 #
#                                       #
#########################################


class PostBase(BaseModel):
    title: str
    description: str
    content: str
    status: str = "unpublished"

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    content: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True


#########################################
#                                       #
#                 Users                 #
#                                       #
#########################################


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        orm_mode = True


#########################################
#                                       #
#             Relationships             #
#                                       #
#########################################


class User(UserBase):
    id: int
    posts: List[PostBase] = []


class Post(PostBase):
    id: int
    created: date
    updated: date
    author: UserBase

    class Config:
        orm_mode = True
