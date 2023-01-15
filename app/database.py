from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import config

engine = create_engine(f"postgresql://{config.DATABASE_USERNAME}:%s@{config.DATABASE_HOSTNAME}/{config.DATABASE_NAME}" % quote_plus(f"{config.DATABASE_PASSWORD}"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
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