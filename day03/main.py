from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

"""
Query() → validation/configuration for query parameters
Path()  → validation/configuration for path parameters
Field() → validation/configuration for Pydantic model fields

---------Flow----------
FastAPI receives the request → Pydantic validates the data → a Pydantic object is created 
→ the endpoint function receives it → we can process it or convert it with model_dump() → FastAPI returns the response.
"""


class Address(BaseModel):
    city: str
    country: str
    postal_code: str = Field(min_length=5, max_length=5)


# BaseModel is the base class provided by Pydantic for creating data models. It gives the model data validation, parsing, and structured fields.
# The student class inherits from BaseModel, that makes it a pydantic model
class Student(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(ge=18, le=100)
    email: EmailStr
    phone: str | None = None
    address: Address


class Course(BaseModel):
    title: str = Field(min_length=3)
    credits: int = Field(ge=1, le=10)
    instructor_email: EmailStr
    description: str | None = None
    student: Student


@app.post("/students")
def create_student(student: Student):  # The request body should contain data that matches the Student Pydantic model
    data = student.model_dump()  # student.model_dump() converts that object into a Python dictionary, which FastAPI can return as JSON.
    return data


@app.post("/courses")
def create_course(course: Course):
    data = course.model_dump()
    return data
