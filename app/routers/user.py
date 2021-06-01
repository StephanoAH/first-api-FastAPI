from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session


router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "/register",
    response_model=schemas.UserBase,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashing.bcrypt(user.password),
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


@router.get(
    "/",
    response_model=List[schemas.User],
    status_code=status.HTTP_200_OK,
)
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users in the database",
        )
    return users


@router.get(
    "/{id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
def get_specific_users(id, db: Session = Depends(database.get_db)):
    users = db.query(models.User).filter(models.User.id == id).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} was not found"
        )
    return users


@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    update = db.query(models.User).filter(models.User.id == id)
    if not update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} does not exist"
        )
    update.update(user.dict(exclude_unset=True))  #! vars transform schema in a dict
    db.commit()
    return "Updated"


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(database.get_db)):
    db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
    db.commit()
    return "Deleted"
