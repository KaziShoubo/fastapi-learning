from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.student import Student
from ..schemas.student import StudentCreate, StudentUpdate


def get_all_students(db: Session):
    result = db.execute(select(Student))
    students = result.scalars().all()  # turns the database result into a Python list of Student ORM objects.
    return students


def get_student(student_id: int, db: Session):
    res = select(Student).where(Student.id == student_id)
    result = db.execute(res)
    student = result.scalar_one_or_none()
    return student


def create_student(student_data: StudentCreate, db: Session):
    student = Student(name=student_data.name, age=student_data.age)
    db.add(student)  # Adds the SQLAlchemy object to the current session
    db.commit()  # Make the changes in this transaction permanent in the database.
    db.refresh(student)  # Reloads the object's database values into Python

    return student


def update_student(student_id: int, student_data: StudentUpdate, db: Session):
    res = select(Student).where(Student.id == student_id)
    result = db.execute(res)
    student = result.scalar_one_or_none()  # Return one student or None

    if student is None:
        return None
    student.name = student_data.name
    student.age = student_data.age

    db.commit()
    db.refresh(student)

    return student


def delete_student(student_id: int, db: Session):
    res = select(Student).where(Student.id == student_id)
    result = db.execute(res)
    student = result.scalar_one_or_none()

    if student is None:
        return None

    db.delete(student)
    db.commit()  # persists the changes
    return {"message": "Student is deleted!"}
