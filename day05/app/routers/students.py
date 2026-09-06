# HTTP endpoints, parameters, HTTP errors

from fastapi import APIRouter, HTTPException, Query
from ..services.student_service import get_all_students, create_student, get_student, update_student, delete_student,\
    search_students
from ..schemas.student import StudentResponse, StudentCreate, StudentUpdate

# APIRouter lets us group related API endpoints into separate modules instead of putting everything in main.py
router = APIRouter(prefix="/students")


@router.get("", response_model=list[StudentResponse])
def get_students():
    return get_all_students()


@router.get("/search", response_model=list[StudentResponse])
def search_student_endpoint(min_age: int = Query(0, ge=0, le=100), max_age: int = Query(100, ge=0, le=100)):
    return search_students(min_age, max_age)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student_endpoint(student_id: int):
    student = get_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")

    return student


@router.post("", response_model=StudentResponse)
def create_student_endpoint(student: StudentCreate):
    return create_student(student)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student_endpoint(student_id: int, student_obj: StudentUpdate):
    student = update_student(student_id, student_obj)
    if student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")

    return student


@router.delete("/{student_id}")
def delete_student_endpoint(student_id: int):
    student = delete_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")

    return student
