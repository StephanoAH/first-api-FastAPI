from typing import List
from fastapi import APIRouter, Depends, status
from .. import schemas, database, JWTtoken
from sqlalchemy.orm import Session
from ..actions import blog


router = APIRouter(prefix="/post", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostBase, db: Session = Depends(database.get_db)):
    return blog.create(post, db)


@router.get("/", response_model=List[schemas.Post], status_code=status.HTTP_200_OK)
def get_all_post(
    db: Session = Depends(database.get_db),
    get_current_user: schemas.User = Depends(JWTtoken.get_current_user),
):
    return blog.get_all(db)


@router.get("/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def get_specific_post(id, db: Session = Depends(database.get_db)):
    return blog.get_one(id, db)


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id, post: schemas.PostUpdate, db: Session = Depends(database.get_db)):
    return blog.update(id, post, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(database.get_db)):
    return blog.delete(id, db)
