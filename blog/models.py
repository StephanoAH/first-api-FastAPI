import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    content = Column(String)
    status = Column(String)
    created = Column(Date, default=datetime.datetime.now)
    updated = Column(
        Date, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    posts = relationship("Post", back_populates="author")
