from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, hashing


def login(request: schemas.UserLogin, db: Session):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email"
        )
    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password"
        )
    return user
