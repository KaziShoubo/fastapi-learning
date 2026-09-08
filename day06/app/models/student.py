from sqlalchemy import Column, Integer, String
from ..database.database import Base


class Student(Base):                        # Tells - Student is database model
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
