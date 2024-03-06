from typing import List

from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    session: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = None,
):
    posts = None
    posts_query = session.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id)
    if search:
        posts = posts_query.filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()
    else:
        posts = posts_query.order_by(models.Post.id).limit(limit).offset(skip).all()
    posts = list(map(lambda x : x._mapping, posts))
    return posts


@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    session: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = models.Post(title=post.title, content=post.content, published=post.published, owner_id=current_user.id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, session: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = session.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = session.query(models.Post).filter_by(id=id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action.",
        )
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, session: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    _post = session.query(models.Post).filter_by(id=id).first()
    if not _post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
    if _post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action.",
        )
    _post.title = post.title
    _post.content = post.content
    _post.published = post.published
    session.commit()
    session.refresh(_post)
    return _post
