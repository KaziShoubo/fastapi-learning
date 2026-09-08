# Day 6 — SQLite & SQLAlchemy

##  Goals

- Understand SQLite databases
- Understand SQLAlchemy and ORM
- Create SQLAlchemy database models
- Create a SQLite database
- Create database sessions
- Use FastAPI dependency injection for database sessions
- Perform database CRUD operations
- Move database logic into the service layer
- Understand database persistence

---

##  Project Structure

```text
day06/
└── app/
    ├── __init__.py
    ├── main.py
    │
    ├── database/
    │   ├── __init__.py
    │   └── database.py
    │
    ├── models/
    │   ├── __init__.py
    │   └── student.py
    │
    ├── routers/
    │   ├── __init__.py
    │   └── students.py
    │
    ├── schemas/
    │   ├── __init__.py
    │   └── student.py
    │
    └── services/
        ├── __init__.py
        └── student_service.py

students.db