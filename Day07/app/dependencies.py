from sqlalchemy.orm import Session
from fastapi import Depends
from .database.database import get_db


def get_message():
    return "Hello from dependency"


def get_user():
    return {
        "username": "Shoubo",
        "role": "student"
    }


def get_current_user(db: Session = Depends(get_db)):
    return {
        "username": "Shoubo",
        "role": "student"
    }


def get_admin_user():
    return {
        "username": "Shoubo",
        "role": "admin"
    }
