from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import config

engine = create_engine(f"postgresql+psycopg2://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOSTNAME}:{config.DATABASE_PORT}/{config.DATABASE_NAME}")

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
        conn =  psycopg2.connect(port= config.DATABASE_PORT, host = config.DATABASE_HOSTNAME, database = config.DATABASE_NAME, user = config.DATABASE_USERNAME, password= config.DATABASE_PASSWORD, cursor_factory=RealDictCursor) 
        cursor = conn.cursor()
        print('Database connection was successfull')
        break

    except Exception as error:
        print('Connecting to database failed')
        print('ERROR:', error)
        time.sleep(2)