from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Alice", "age": 25, "password": "s111"},
    {"id": 2, "name": "Bob", "age": 23, "password": "s121"},
    {"id": 3, "name": "Charlie", "age": 24, "password": "s113"}
]


class StudentCreate(BaseModel):
    name: str
    age: int


class StudentUpdate(BaseModel):
    name: str
    age: int


# This model is useful when we have some data in our database or list which we don't want to send to the client
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int


# The response from this endpoint should follow the StudentResponse model
# For an endpoint returning multiple students
@app.get("/students", response_model=list[StudentResponse])
def get_students():
    return students


# Specific/static routes should be declared before dynamic routes when they could otherwise be captured by the path parameter.
@app.get("/students/search", response_model=list[StudentResponse])
def search_student(min_age: int = Query(0, ge=0, le=100), max_age: int = Query(100, ge=0, le=100)):
    result = []

    for student in students:
        if min_age <= student["age"] <= max_age:
            result.append(student)

    return result


# For endpoints returning a student
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    # If student not found
    raise HTTPException(
        status_code=404,
        detail="Student Not Found"
    )


@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate):
    # 1. Generating a new id
    # Generate all ids
    ids = [student["id"] for student in students]  # List Comprehension
    # find max id
    max_id = max(ids)
    # create new id
    new_id = max_id + 1

    # 2. Create a dictionary
    new_student = {
        "id": new_id,
        "name": student.name,
        "age": student.age
    }

    # 3. Adding it to the students
    students.append(new_student)

    # 4. returning the newly created student
    return new_student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate):
    for stu in students:
        if stu["id"] == student_id:
            stu["name"] = student.name
            stu["age"] = student.age
            return stu

    raise HTTPException(
        status_code=404,
        detail="Student Not Found"
    )


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": "Student deleted successfully",
                    "student_id": student_id}

    raise HTTPException(
        status_code=404,
        detail="Student Not Found"
    )
