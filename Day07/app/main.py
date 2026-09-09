from fastapi import FastAPI, Depends
# from .routers.router import router
from sqlalchemy.orm import Session
from .database.database import get_db
from .dependencies import get_user, get_current_user, get_admin_user

app = FastAPI()


# app.include_router(router)


@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    return {
        "message": "Database dependency works"
    }


@app.get("/db-info")
def database_info(db: Session = Depends(get_db)):
    return {
        "database": "SQLite",
        "status": "connected"
    }


@app.get("/user-info")
def get_user_info(user: dict = Depends(get_user)):
    return user


@app.get("/current-user")
def get_current_user_info(user: dict = Depends(get_current_user)):
    return user


@app.get("/admin")
def get_admin_user_info(admin_user: dict = Depends(get_admin_user)):
    return admin_user
