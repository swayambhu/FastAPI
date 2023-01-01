from ..database import get_db
from .. import models
from sqlalchemy.orm import Session
from ..utils import hash
from fastapi import status, HTTPException, Depends, APIRouter
from ..schemas import UserCreate, UserOut

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.password
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    user_already_exist = db.query(models.User).filter(models.User.email == new_user.email).first()
    if user_already_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with this emai already exists")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model= UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user
    