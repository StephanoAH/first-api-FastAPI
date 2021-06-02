from fastapi import APIRouter, Depends, status
from .. import schemas, database
from sqlalchemy.orm import Session
from ..actions import auth


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(request: schemas.UserLogin, db: Session = Depends(database.get_db)):
    return auth.login(request, db)
