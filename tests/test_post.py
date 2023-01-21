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
    
def test_unauthorised_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary titel", "content": "content"})
    
    assert res.status_code == 401
    

def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
    
    
def test_delete_post_success(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204
    
def test_delete_post_non_exists(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/99999")
    
    assert res.status_code == 404
    
def test_delete_other_user_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[3].id}")
    
    assert res.status_code == 403
    
def test_update_post(authorised_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content" : "updated content",
        "id" : test_posts[0].id
    }
    
    res = authorised_client.put(f'/posts/{test_posts[0].id}', json=data)
    
    updated_post = schemas.Post(**res.json())
    
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    
def test_update_other_user_post(authorised_client, test_user, test_posts, test_user2):
    data = {
        "title": "updated title",
        "content" : "updated content",
        "id" : test_posts[3].id
    }
    
    res = authorised_client.put(f'/posts/{test_posts[3].id}', json=data)
    
    assert res.status_code == 403
   
def test_unauthorised_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content" : "updated content",
        "id" : test_posts[3].id
    }
    res = client.put(f"/posts/{test_posts[0].id}",  json=data)
    assert res.status_code == 401
    
def test_update_post_non_exists(authorised_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content" : "updated content",
        "id" : test_posts[3].id
    }
    res = authorised_client.put(f"/posts/99999",  json=data)
    
    assert res.status_code == 404