# Business/data operations

from ..schemas.student import StudentCreate, StudentUpdate

students = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 23}
]


def get_all_students():
    return students


def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def search_students(min_age: int, max_age: int):
    result = []
    for student in students:
        if max_age >= student["age"] >= min_age:
            result.append(student)

    return result


def create_student(student: StudentCreate):
    ids = [student["id"] for student in students]
    max_id = max(ids)
    new_id = max_id + 1

    new_student = {
        "id": new_id,
        "name": student.name,
        "age": student.age
    }

    students.append(new_student)
    return new_student


def update_student(student_id: int, student_obj: StudentUpdate):
    for student in students:
        if student["id"] == student_id:
            student["name"] = student_obj.name
            student["age"] = student_obj.age
            return student

    return None


def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"Message": "Successfully deleted", "id": student_id}

    return None
