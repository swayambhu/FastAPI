from fastapi.testclient import TestClient
from app.main import app
from app import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app import models
from app.oauth2 import create_access_token
import pytest
from app import models


TEST_SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{config.DATABASE_USERNAME}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOSTNAME}:{config.DATABASE_PORT}/fastapi_test"


engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        
@pytest.fixture()
def session():
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    

@pytest.fixture
def test_user(client):
    user_data = {"email": "swayambhu43@gmail.com", "password": "password123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }
    
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "My first post",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "My second post",
            "content": "second content",
            "owner_id": test_user['id']
        },
        {
            "title": "My third post",
            "content": "third content",
            "owner_id": test_user['id']
        }
    ]
    
    def create_posts_model(post):
        return models.Posts(**post)
        
    post_map = map(create_posts_model, posts_data)
    
    posts = list(post_map)
    
    session.add_all(posts)
    
    session.commit()
    
    posts = session.query(models.Posts).all()
    
    return posts