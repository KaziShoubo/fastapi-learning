from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

students = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 19},
    {"id": 3, "name": "Charlie", "age": 22},
    {"id": 4, "name": "David", "age": 30},
    {"id": 5, "name": "Emma", "age": 21},
]


@app.get("/students")
def get_students(min_age: int = Query(0, ge=0, le=50),
                 limit: int = Query(10, ge=1, le=100),
                 offset: int = Query(0, ge=0),
                 sort: str = Query("id")
                 ):
    # ----Filtering------
    # Checking min_age
    results = []
    for student in students:
        if student["age"] >= min_age:
            results.append(student)

    # -------Sorting------
    # Determine sorting direction:
    # "-" at the beginning means descending order
    reverse = sort.startswith("-")

    # Remove "-" to get the actual field name (e.g. "-age" → "age")
    sort_field = sort.lstrip("-")

    # Sort students by the requested field
    if sort_field == "age":
        results = sorted(
            results,
            key=lambda student: student["age"],
            reverse=reverse
        )

    elif sort_field == "name":
        results = sorted(
            results,
            key=lambda student: student["name"],
            reverse=reverse
        )

    else:
        raise HTTPException(
            status_code=422,
            detail="Invalid sort field. Use age or name."

        )

    # --------Pagination----------
    results = results[offset:offset + limit]  # That's how offset and limit is counted and we are using slicing here

    return results
