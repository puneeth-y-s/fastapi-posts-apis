from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, session: Session = Depends(get_db)):
    try:
        user = session.query(models.User).filter_by(id=id).one()
    except NoResultFound:
        raise HTTPException(
            detail=f"user with id {id} was not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return user
