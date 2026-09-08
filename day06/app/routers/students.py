from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..schemas.student import StudentCreate, StudentResponse, StudentUpdate
from ..services.student_service import get_all_students, get_student, create_student, update_student, delete_student

router = APIRouter()


@router.get("/students")
def get_students(db: Session = Depends(get_db)):  # call get_db() and give the database session
    return get_all_students(db)


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    student = get_student(student_id, db)
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.post("/students", response_model=StudentResponse)
def create_student_endpoint(student_data: StudentCreate, db: Session = Depends(get_db)):
    student = create_student(student_data, db)
    return student


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student_endpoint(student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    student = update_student(student_id, student_data, db)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.delete("/students/{student_id}")
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    student = delete_student(student_id, db)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


