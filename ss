[1mdiff --git a/Terminal_comment b/Terminal_comment[m
[1mindex 0cfce50..6cfe290 100644[m
[1m--- a/Terminal_comment[m
[1m+++ b/Terminal_comment[m
[36m@@ -1,6 +1,7 @@[m
 When I want to run my server:[m
 [m
 fastapi dev day01/main.py           (just need to change the file name everytime)[m
[32m+[m[32muvicorn app.main:app --reload[m
 [m
 When I want to stop my server:  ctrl+c[m
 [m
[1mdiff --git a/day05/README.md b/day05/README.md[m
[1mindex e69de29..53e0b26 100644[m
[1m--- a/day05/README.md[m
[1m+++ b/day05/README.md[m
[36m@@ -0,0 +1,47 @@[m
[32m+[m[32m## Day 5 — Professional FastAPI Project Structure[m
[32m+[m
[32m+[m[32m### Goals[m
[32m+[m[32m- Understand professional FastAPI project structure[m
[32m+[m[32m- Use APIRouter[m
[32m+[m[32m- Separate routers, schemas, and services[m
[32m+[m[32m- Use include_router()[m
[32m+[m[32m- Use router prefixes[m
[32m+[m[32m- Separate HTTP logic from business logic[m
[32m+[m[32m- Implement CRUD using a layered structure[m
[32m+[m[32m- Implement student search/filtering[m
[32m+[m
[32m+[m[32m### Project Structure[m
[32m+[m
[32m+[m[32mday05/[m
[32m+[m[32m└── app/[m
[32m+[m[32m    ├── main.py[m
[32m+[m[32m    ├── routers/[m
[32m+[m[32m    │   └── students.py[m
[32m+[m[32m    ├── schemas/[m
[32m+[m[32m    │   └── student.py[m
[32m+[m[32m    └── services/[m
[32m+[m[32m        └── student_service.py[m
[32m+[m
[32m+[m[32m### Architecture[m
[32m+[m
[32m+[m[32mRouter → Schema → Service → Data[m
[32m+[m
[32m+[m[32m### Implemented Endpoints[m
[32m+[m
[32m+[m[32m- GET /students[m
[32m+[m[32m- GET /students/{student_id}[m
[32m+[m[32m- GET /students/search[m
[32m+[m[32m- POST /students[m
[32m+[m[32m- PUT /students/{student_id}[m
[32m+[m[32m- DELETE /students/{student_id}[m
[32m+[m
[32m+[m[32m### Key Concepts Learned[m
[32m+[m
[32m+[m[32m- APIRouter[m
[32m+[m[32m- include_router()[m
[32m+[m[32m- Router prefixes[m
[32m+[m[32m- Layered architecture[m
[32m+[m[32m- Separation of concerns[m
[32m+[m[32m- Service layer[m
[32m+[m[32m- Schema layer[m
[32m+[m[32m- HTTPException handling[m
\ No newline at end of file[m
[1mdiff --git a/day05/app/main.py b/day05/app/main.py[m
[1mindex e69de29..3060b81 100644[m
[1m--- a/day05/app/main.py[m
[1m+++ b/day05/app/main.py[m
[36m@@ -0,0 +1,8 @@[m
[32m+[m[32m# Create app + register routers[m
[32m+[m
[32m+[m[32mfrom fastapi import FastAPI[m
[32m+[m[32mfrom .routers.students import router[m
[32m+[m
[32m+[m[32mapp = FastAPI()[m
[32m+[m
[32m+[m[32mapp.include_router(router)[m
\ No newline at end of file[m
[1mdiff --git a/day05/app/routers/students.py b/day05/app/routers/students.py[m
[1mindex e69de29..1e8c571 100644[m
[1m--- a/day05/app/routers/students.py[m
[1m+++ b/day05/app/routers/students.py[m
[36m@@ -0,0 +1,51 @@[m
[32m+[m[32m# HTTP endpoints, parameters, HTTP errors[m
[32m+[m
[32m+[m[32mfrom fastapi import APIRouter, HTTPException, Query[m
[32m+[m[32mfrom ..services.student_service import get_all_students, create_student, get_student, update_student, delete_student,\[m
[32m+[m[32m    search_students[m
[32m+[m[32mfrom ..schemas.student import StudentResponse, StudentCreate, StudentUpdate[m
[32m+[m
[32m+[m[32m# APIRouter lets us group related API endpoints into separate modules instead of putting everything in main.py[m
[32m+[m[32mrouter = APIRouter(prefix="/students")[m
[32m+[m
[32m+[m
[32m+[m[32m@router.get("", response_model=list[StudentResponse])[m
[32m+[m[32mdef get_students():[m
[32m+[m[32m    return get_all_students()[m
[32m+[m
[32m+[m
[32m+[m[32m@router.get("/search", response_model=list[StudentResponse])[m
[32m+[m[32mdef search_student_endpoint(min_age: int = Query(0, ge=0, le=100), max_age: int = Query(100, ge=0, le=100)):[m
[32m+[m[32m    return search_students(min_age, max_age)[m
[32m+[m
[32m+[m
[32m+[m[32m@router.get("/{student_id}", response_model=StudentResponse)[m
[32m+[m[32mdef get_student_endpoint(student_id: int):[m
[32m+[m[32m    student = get_student(student_id)[m
[32m+[m[32m    if student is None:[m
[32m+[m[32m        raise HTTPException(status_code=404, detail="Student Not Found")[m
[32m+[m
[32m+[m[32m    return student[m
[32m+[m
[32m+[m
[32m+[m[32m@router.post("", response_model=StudentResponse)[m
[32m+[m[32mdef create_student_endpoint(student: StudentCreate):[m
[32m+[m[32m    return create_student(student)[m
[32m+[m
[32m+[m
[32m+[m[32m@router.put("/{student_id}", response_model=StudentResponse)[m
[32m+[m[32mdef update_student_endpoint(student_id: int, student_obj: StudentUpdate):[m
[32m+[m[32m    student = update_student(student_id, student_obj)[m
[32m+[m[32m    if student is None:[m
[32m+[m[32m        raise HTTPException(status_code=404, detail="Student Not Found")[m
[32m+[m
[32m+[m[32m    return student[m
[32m+[m
[32m+[m
[32m+[m[32m@router.delete("/{student_id}")[m
[32m+[m[32mdef delete_student_endpoint(student_id: int):[m
[32m+[m[32m    student = delete_student(student_id)[m
[32m+[m[32m    if student is None:[m
[32m+[m[32m        raise HTTPException(status_code=404, detail="Student Not Found")[m
[32m+[m
[32m+[m[32m    return student[m
[1mdiff --git a/day05/app/schemas/student.py b/day05/app/schemas/student.py[m
[1mindex 6a56be1..91494ff 100644[m
[1m--- a/day05/app/schemas/student.py[m
[1m+++ b/day05/app/schemas/student.py[m
[36m@@ -1,3 +1,5 @@[m
[32m+[m[32m# Pydantic validation/data structure[m
[32m+[m
 from pydantic import BaseModel[m
 [m
 [m
[1mdiff --git a/day05/app/services/student_service.py b/day05/app/services/student_service.py[m
[1mindex e69de29..c3e5687 100644[m
[1m--- a/day05/app/services/student_service.py[m
[1m+++ b/day05/app/services/student_service.py[m
[36m@@ -0,0 +1,62 @@[m
[32m+[m[32m# Business/data operations[m
[32m+[m
[32m+[m[32mfrom ..schemas.student import StudentCreate, StudentUpdate[m
[32m+[m
[32m+[m[32mstudents = [[m
[32m+[m[32m    {"id": 1, "name": "Alice", "age": 25},[m
[32m+[m[32m    {"id": 2, "name": "Bob", "age": 23}[m
[32m+[m[32m][m
[32m+[m
[32m+[m
[32m+[m[32mdef get_all_students():[m
[32m+[m[32m    return students[m
[32m+[m
[32m+[m
[32m+[m[32mdef get_student(student_id: int):[m
[32m+[m[32m    for student in students:[m
[32m+[m[32m        if student["id"] == student_id:[m
[32m+[m[32m            return student[m
[32m+[m[32m    return None[m
[32m+[m
[32m+[m
[32m+[m[32mdef search_students(min_age: int, max_age: int):[m
[32m+[m[32m    result = [][m
[32m+[m[32m    for student in students:[m
[32m+[m[32m        if max_age >= student["age"] >= min_age:[m
[32m+[m[32m            result.append(student)[m
[32m+[m
[32m+[m[32m    return result[m
[32m+[m
[32m+[m
[32m+[m[32mdef create_student(student: StudentCreate):[m
[32m+[m[32m    ids = [student["id"] for student in students][m
[32m+[m[32m    max_id = max(ids)[m
[32m+[m[32m    new_id = max_id + 1[m
[32m+[m
[32m+[m[32m    new_student = {[m
[32m+[m[32m        "id": new_id,[m
[32m+[m[32m        "name": student.name,[m
[32m+[m[32m        "age": student.age[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    students.append(new_student)[m
[32m+[m[32m    return new_student[m
[32m+[m
[32m+[m
[32m+[m[32mdef update_student(student_id: int, student_obj: StudentUpdate):[m
[32m+[m[32m    for student in students:[m
[32m+[m[32m        if student["id"] == student_id:[m
[32m+[m[32m            student["name"] = student_obj.name[m
[32m+[m[32m            student["age"] = student_obj.age[m
[32m+[m[32m            return student[m
[32m+[m
[32m+[m[32m    return None[m
[32m+[m
[32m+[m
[32m+[m[32mdef delete_student(student_id: int):[m
[32m+[m[32m    for student in students:[m
[32m+[m[32m        if student["id"] == student_id:[m
[32m+[m[32m            students.remove(student)[m
[32m+[m[32m            return {"Message": "Successfully deleted", "id": student_id}[m
[32m+[m
[32m+[m[32m    return None[m
