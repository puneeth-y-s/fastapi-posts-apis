from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Srim@ntudu112358",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed.")
        print("Error", error)
        time.sleep(2)


posts = [
    {
        "title": "Favorite holiday destination",
        "content": "India",
        "id": 1
    },
    {
        "title": "Favorite foods",
        "content": "I like Pizza",
        "id": 2
    },
]


def find_index_post(id):
    for index, post in enumerate(posts):
        if post["id"] == id:
            return index


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/")
def root():
    return {"message": "Welcome to fast api"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = (%s)", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = (%s)", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
    cursor.execute("DELETE FROM posts WHERE id = (%s)", (id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("SELECT * FROM posts WHERE id = (%s)", (id,))
    old_post = cursor.fetchone()
    if not old_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
    cursor.execute("UPDATE posts SET title = (%s), content = (%s), published = (%s) WHERE id = (%s) RETURNING *", (post.title, post.content, post.published, id))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}