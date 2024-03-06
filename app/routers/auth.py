from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from sqlalchemy.exc import NoResultFound
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm stores email in username field
    user = session.query(models.User).filter_by(email=user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials!!"
        )
    if not utils.verify_password_hash(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials!!"
        )
    # create and return jwt token
    access_token = oauth2.create_access_token(
        data = {"user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
