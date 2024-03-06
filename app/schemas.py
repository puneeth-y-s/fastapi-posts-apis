from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User related pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode= True

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode= True

# login related pydantic models
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode= True

# token related pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode= True

class TokenData(BaseModel):
    id: Optional[str] = None

    class Config:
        orm_mode= True

# Post related pydantic models
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode= True

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

# vote_dir = 0 means downvote
# vote_dir = 1 means upvote
class Vote(BaseModel):
    post_id: int
    vote_dir: int