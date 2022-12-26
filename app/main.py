from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

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






@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
def get_posts( db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts  =  cursor.fetchall()
    posts = db.query(models.Posts).all()
    return {"data": posts}



    
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""
    #                INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING *
    #                """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()

    
    new_post = models.Posts(**post.dict())
    db.add(new_post) #add post to database
    db.commit() #commit post to database
    db.refresh(new_post) #assign created post to variable
    
    return {"data": new_post}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""
                    SELECT * FROM posts ORDER BY id DESC LIMIT 5
                   """)
    
    posts = cursor.fetchall()

    return {"data": posts}

@app.get("/posts/{id}")
def find_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"data" : "post not found"})
    return {"data": post}

    


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db)):
    
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Posts).filter(models.Posts.id == id)    
    
    if not post.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"post_detail" : "post not found"})
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    
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