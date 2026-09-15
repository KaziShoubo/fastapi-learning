from app.models import Student
# TestClient allows us to send HTTP requests to our FastAPI application without manually starting Uvicorn.

#-----------Normal Tests------------
# Testing get requests (successful response)
def test_about(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI Testing"}  # it converts the response body into a Python object.

# we test when the endpoint is invalid (unsuccessful response)
def test_invalid_endpoint(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404


# Testing response data
def test_get_users(client):
    response = client.get("/users")

    data = response.json()

    assert response.status_code == 200
    assert data["username"] == "Samiha"
    assert data["role"] == "student"


# Testing post requests
def test_create_user(client):
    response = client.post(
        "/users",
        json={"username": "Samiha", "role": "student"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "user created", "username": "Samiha", "role": "student"}


# Testing validation error (a missing field)
def test_create_user_missing_role(client):
    response = client.post(
        "/users",
        json={"username": "Samiha"}
    )

    # print(response.json())
    assert response.status_code == 422

    data = response.json()

    assert data["detail"][0]["loc"] == ["body", "role"]
    assert data["detail"][0]["msg"] == "Field required"

# Fixture dependencies → one fixture/test can use another fixture
def test_user_fixture(test_user):
    assert test_user["username"] == "Samiha"
    assert test_user["role"] == "student"



#------------------Database Tests----------------------

"""
Step 1: Database configuration 
Step 2: SQLAlchemy model 
Step 3: FastAPI gets a DB session 
Step 4: Query students
Step 5: Write tests
Step 6: Override get_db() with a test database 
"""


def test_create_student(client, setup_test_database):
    response = client.post(
        "/students",
        json={
            "name": "Alice",
            "age": 25
        }
    )

    data = response.json()
    assert response.status_code == 200

    assert data["name"] == "Alice"
    assert data["age"] == 25


def test_get_students(client, setup_test_database):
    response = client.get("/students")

    assert response.status_code == 200

# prove the test database is isolated
def test_database_isolation(client, setup_test_database, db_session):
    student = Student(
        name="Test Student",
        age= 30
    )

    db_session.add(student)
    db_session.commit()
    response = client.get("/students")

    data = response.json()

    # any()- Does any returned student have this name and age?
    assert any(
        student["name"] == "Test Student" and student["age"] == 30
        for student in data
    )








