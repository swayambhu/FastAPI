from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn =  psycopg2.connect(host ='localhost', database = 'fastapi', user = 'postgres', password='S@wayambhu2000@1@2@3', cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        
        print('Database connection was successfull')
        break

    except Exception as error:
        print('Connecting to database failed')
        print('ERROR:', error)
        time.sleep(2)

    
my_posts = [
    {
        'title': 'title of post 1', 
        'content': 'content of post 1',
        'id': 1
    },
    {
        'title': 'title of post 2', 
        'content': 'content of post 2',
        'id': 2
    },
]

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts  =  cursor.fetchall()
    return {"data": posts}



    
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""
                   INSERT INTO posts (title, content, published) 
                   VALUES (%s, %s, %s) RETURNING *
                   """, (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    
    conn.commit()
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"detail": post}

@app.get("/posts/{id}")
def find_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"data" : "post not found"})
    return {"data": post}

    


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if not deleted_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"post_detail" : "post not found"})
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""
                        UPDATE posts SET 
                        title = %s, content = %s, published = %s 
                        WHERE id = %s RETURNING *
                   """, 
                   (post.title, post.content, post.published, str(id))
                )
    
    updated_post = cursor.fetchone()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail={"post_detail": "post not found"})
    
    return {"data" : updated_post}