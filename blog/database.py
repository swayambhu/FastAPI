from sqlalchemy import create_engine

DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/cricket"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})