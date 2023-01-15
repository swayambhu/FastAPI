from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import Post, PostCreate
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..oauth2 import get_current_user



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[Post])
def get_posts( db: Session = Depends(get_db),current_user = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts  =  cursor.fetchall()
    print(limit)
    # posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).limit(limit).offset(skip).all()
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts



    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: dict =  Depends(get_current_user)):
    # cursor.execute("""
    #                INSERT INTO posts (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING *
    #                """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()
    
    
    new_post = models.Posts(owner_id=current_user.id, **post.dict())
    db.add(new_post) #add post to database
    db.commit() #commit post to database
    db.refresh(new_post) #assign created post to variable
    
    return new_post


@router.get("/latest")
def get_latest_post():
    cursor.execute("""
                    SELECT * FROM posts ORDER BY id DESC LIMIT 5
                   """)
    
    posts = cursor.fetchall()

    return posts

@router.get("/{id}", response_model=Post)
def find_post(id: int, response: Response, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"data" : "post not found"})
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    return post

    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int =  Depends(get_current_user)):
    
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Posts).filter(models.Posts.id == id)    
    
    post = post_query.first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= {"post_detail" : "post not found"})
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model= Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(get_current_user)):
    
    # cursor.execute("""
    #                     UPDATE posts SET 
    #                     title = %s, content = %s, published = %s 
    #                     WHERE id = %s RETURNING *
    #                """, 
    #                (post.title, post.content, post.published, str(id))
    #             )
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    
    updated_post = post_query.first()

        
    if not updated_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail={"post_detail": "post not found"})
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()