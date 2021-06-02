from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models


def create(post: schemas.PostBase, db: Session):
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


def get_all(db: Session):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not have any post yet",
        )
    return posts


def get_one(id, db: Session):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} was not found"
        )
    return post


def update(id, post: schemas.PostUpdate, db: Session):
    update = db.query(models.Post).filter(models.Post.id == id)
    if not update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist"
        )
    update.update(
        post.dict(exclude_unset=True)
    )  #! Create a dict using the data that was set when creating the schema excluding default values
    db.commit()
    return "Updated"


def delete(id, db: Session):
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted"
