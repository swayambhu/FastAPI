from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, users


models.Base.metadata.create_all(engine)

app = FastAPI()



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





app.include_router(post.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


