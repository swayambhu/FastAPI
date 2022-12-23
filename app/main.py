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
    return {"data": my_posts}



    
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(my_posts)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return {"detail": post}

@app.get("/posts/{id}")
def find_post(id: int, response: Response):
    try:
        post = my_posts[id - 1]
        return {"post_detail": post}
    except IndexError:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"post_detail" : "post not found"})
    


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    try:
        deleted_post = my_posts.pop(id - 1)
        return {"deleted_post": delete_post}
    except IndexError:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"post_detail" : "post not found"})
    

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    try:
        my_posts[id - 1] = post
        return {"message" : post}
    except IndexError:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail={"post_detail": "post not found"})