from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, hashing


def register(users: schemas.UserCreate, db: Session):
    new_user = models.User(
        first_name=users.first_name,
        last_name=users.last_name,
        email=users.email,
        password=hashing.hash_password(users.password),
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


def get_all_users(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users in the database",
        )
    return users


def get_user(id, db: Session):
    users = db.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} was not found"
        )
    return users


def update(id, users: schemas.UserUpdate, db: Session):
    update = db.query(models.User).filter(models.User.id == id)
    if not update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} does not exist"
        )
    update.update(
        users.dict(exclude_unset=True)
    )  #! Create a dict using the data that was set when creating the schema excluding default values
    db.commit()
    return "Updated"


def delete(id, db: Session):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted"
