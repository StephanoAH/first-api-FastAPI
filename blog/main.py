from typing import List
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models, database
from .hashing import bcrypt


app = FastAPI()

models.Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


tags_metadata = [{"name": "Posts"}, {"name": "Users"}]

##############################################################################################
#                                                                                            #
#                                        Post routes                                         #
#                                                                                            #
##############################################################################################


@app.post("/post", status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
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


@app.get(
    "/post",
    response_model=List[schemas.Post],
    status_code=status.HTTP_200_OK,
    tags=["Posts"],
)
def get_all_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not have any post yet",
        )
    return posts


@app.get(
    "/post/{id}",
    response_model=schemas.Post,
    status_code=status.HTTP_200_OK,
    tags=["Posts"],
)
def get_specific_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} was not found"
        )
    return post


@app.patch("/post/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Posts"])
def update_post(id, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    update = db.query(models.Post).filter(models.Post.id == id)
    if not update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist"
        )
    update.update(post.dict(exclude_unset=True))  #! vars transform schema in a dict
    db.commit()
    return "Updated"


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
def delete_post(id, db: Session = Depends(get_db)):
    db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted"


##############################################################################################
#                                                                                            #
#                                        User routes                                         #
#                                                                                            #
##############################################################################################


@app.post(
    "/register",
    response_model=schemas.UserBase,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=bcrypt(user.password),
    )
    check_email = (
        db.query(models.User).filter(models.User.email == new_user.email).first()
    )
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Email already in use, please use another email",
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user", status_code=status.HTTP_200_OK, tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users in the database",
        )
    return users


@app.get(
    "/user/{id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_specific_users(id, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} was not found"
        )
    return users


@app.patch("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
def update_user(id, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    update = db.query(models.User).filter(models.User.id == id)
    if not update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} does not exist"
        )
    update.update(user.dict(exclude_unset=True))  #! vars transform schema in a dict
    db.commit()
    return "Updated"


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted"
