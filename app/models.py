from .database import Base
from sqlalchemy import Integer, Column, Boolean, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default="True")
    created_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    # owner = relationship('User', backref="posts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now())

class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
