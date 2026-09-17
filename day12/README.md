# Day 12 — REST API Design & Production Practices

## Goals

- Understand REST API design principles
- Design resource-oriented API endpoints
- Understand filtering with query parameters
- Understand pagination using `limit` and `offset`
- Understand sorting and ascending/descending order
- Understand API versioning
- Understand environment variables and secrets
- Understand CORS
- Implement filtering, sorting, pagination, and validation in FastAPI

---

## Topics Covered

### 1. REST API Design

REST APIs are designed around resources.



### 2. Path Parameters vs Query Parameters

A path parameter identifies a specific resource:

```GET /students/25```

Here, 25 is the student ID.

Query parameters are used for things such as filtering, pagination, and sorting:

```GET /students?min_age=20```

### 3. Pagination

Returning a very large dataset at once is inefficient.

Two common pagination parameters are:

limit → maximum number of records to return
offset → number of records to skip

Examples:

```GET /students?limit=10&offset=0```

Returns the first 10 students.

```GET /students?limit=10&offset=10```

Returns the next 10 students.

Pagination was implemented using Python list slicing:

```results[offset:offset + limit]```

Python indexes start at 0, and the ending index is excluded.

### 4. CORS (Cross-Origin Resource Sharing)
It controls which frontend origins are allowed to make requests to the API.

For example, if the frontend is running at:

```http://localhost:3000```

CORS can allow that origin:
```
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```