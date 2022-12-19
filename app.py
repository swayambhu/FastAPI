from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World testing"}

inventory = {
    1: {
        "name": "Milk",
        "price": 3.99,
        "brand": "Regular"
    }
}

@app.get("/get-item/{item_id}/{name}")
async def get_item(item_id: int = Path(None, description="The ID of the Item you would like to view")):
    return inventory[item_id]


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished'}

@app.get('/blog/{id}')
def show(id: int, limit: int = 10, published: bool = False, sort: Optional[str] = None):
    return {'data': {id : f"{limit}, {published} blogs"}}



@app.get('/blog/{id}/comments')
def comments(id: int):
    return {'data' : {'1','2'}}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f'blog is created with title as {blog.title}'}
