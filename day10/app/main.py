from fastapi import FastAPI, Depends
from .schemas.users import User
from .database import get_db, Base, engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Student
from .schemas.student import StudentCreate

app = FastAPI()

# This tells SQLAlchemy:
#
# Create the tables represented by my models if they don't already exist.
Base.metadata.create_all(bind=engine)


# ---------------Normal tests--------------
@app.get("/about")
def home():
    return {"message": "FastAPI Testing"}


@app.get("/users")
def get_users():
    return {
        "id": 1,
        "username": "Samiha",
        "role": "student"
    }


@app.post("/users")
def create_user(user: User):
    return {
        "message": "user created",
        "username": user.username,
        "role": user.role
    }


# ------------------database Tests-----------------------

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    result = db.execute(select(Student))
    students = result.scalars().all()

    return students


@app.post("/students")
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    student = Student(name=student_data.name, age=student_data.age)
    db.add(student)
    db.commit()
    db.refresh(student)

    return student
