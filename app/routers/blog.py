from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session


router = APIRouter(prefix="/post", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostBase, db: Session = Depends(database.get_db)):
    new_post = models.Post(
        title=post.title,
        description=post.description,
        content=post.content,
        status=post.status,
        author_id=1,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.Post], status_code=status.HTTP_200_OK)
def get_all_post(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not have any post yet",
        )
    return posts


@router.get("/{id}", response_model=schemas.Post, status_code=status.HTTP_200_OK)
def get_specific_post(id, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} was not found"
        )
    return post


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id, post: schemas.PostUpdate, db: Session = Depends(database.get_db)):
    update = db.query(models.Post).filter(models.Post.id == id)
    if not update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist"
        )
    update.update(post.dict(exclude_unset=True))  #! vars transform schema in a dict
    db.commit()
    return "Updated"


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(database.get_db)):
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted"
