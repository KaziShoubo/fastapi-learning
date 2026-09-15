from fastapi.testclient import TestClient
from day09.app.main import app
from day09.app.schemas.user import UserCreate
from day09.app.models.user import User
from pwdlib import PasswordHash
import jwt

client = TestClient(app)

password_hash = PasswordHash.recommended()

hashed_password = password_hash.hash("TestPassword123")

test_user = User(
    username="testadmin",
    password_hash=hashed_password,
    role="admin"
)

db.add

def test_protected_without_token():
    response = client.get("/protected")

    assert response.status_code == 401
