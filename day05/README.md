## Day 5 — Professional FastAPI Project Structure

### Goals
- Understand professional FastAPI project structure
- Use APIRouter
- Separate routers, schemas, and services
- Use include_router()
- Use router prefixes
- Separate HTTP logic from business logic
- Implement CRUD using a layered structure
- Implement student search/filtering

### Project Structure

day05/
└── app/
    ├── main.py
    ├── routers/
    │   └── students.py
    ├── schemas/
    │   └── student.py
    └── services/
        └── student_service.py

### Architecture

Router → Schema → Service → Data

### Implemented Endpoints

- GET /students
- GET /students/{student_id}
- GET /students/search
- POST /students
- PUT /students/{student_id}
- DELETE /students/{student_id}

### Key Concepts Learned

- APIRouter
- include_router()
- Router prefixes
- Layered architecture
- Separation of concerns
- Service layer
- Schema layer
- HTTPException handling