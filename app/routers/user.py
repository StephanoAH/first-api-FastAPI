from app.actions.blog import delete
from typing import List
from fastapi import APIRouter, Depends, status
from .. import schemas, database
from sqlalchemy.orm import Session
from ..actions import user


router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "/register",
    response_model=schemas.UserBase,
    status_code=status.HTTP_201_CREATED,
)
def create_user(users: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return user.register(users, db)


@router.get(
    "/",
    response_model=List[schemas.User],
    status_code=status.HTTP_200_OK,
)
def get_all_users(db: Session = Depends(database.get_db)):
    return user.get_all_users(db)


@router.get(
    "/{id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
def get_specific_users(id, db: Session = Depends(database.get_db)):
    return user.get_user(id, db)


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id, users: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    return user.update(id, users, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(database.get_db)):
    return user.delete(id, db)
