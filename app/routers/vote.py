from fastapi import status, HTTPException, APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from .. import models, schemas

router = APIRouter()

@router.post("/vote")
def vote(vote: schemas.Vote, session: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post = session.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found"
        )

    vote_exists = session.query(models.Vote).filter(models.Vote.user_id == current_user.id).filter(models.Vote.post_id == vote.post_id).first()

    if vote.vote_dir == 0:
        if vote_exists:
            session.delete(vote_exists)
            session.commit()
            return {"message": "successfully deleted post"}
        else:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"post with id {vote.post_id} not found"
            )

    if vote.vote_dir == 1:
        if not vote_exists:
            vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
            session.add(vote)
            session.commit()
            return {"message": "successfully added vote"}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}"
            )

