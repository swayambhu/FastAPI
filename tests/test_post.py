from typing import List
from app import schemas
import pytest
def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")
    
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    
    posts_list = list(posts_map)
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    

def test_get_one_post_not_exist(authorised_client, test_posts):
    res = authorised_client.get(f'/posts/8888')
    assert res.status_code == 404
    

def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.content == test_posts[0].content
    assert post.Posts.title == test_posts[0].title
    

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("awesome new title 2", "None", False),
    ("None", "awesome new content", True),
    ("None", "None", False),
    
])
def test_create_post(authorised_client, test_user, test_posts, title, content, published):
    res = authorised_client.post("/posts/", json={"title": title, "content": content, "published": published})
    
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    

def test_create_post_default_published_true(authorised_client, test_user, test_posts):
    res = authorised_client.post("/posts/", json={"title": "arbitrary title", "content": "content"})
    
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']