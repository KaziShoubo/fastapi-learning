from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Create/use students.db in the current working directory
DATABASE_URL = "sqlite:///./students.db"

# The engine is essentially the object SQLAlchemy uses to communicate with the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# sessionmaker is essentially a factory for creating database sessions.
# SessionLocal can create sessions i.e, Session 1, Session 2...., and a session is what we will use to interact with the Database.
# bind=engine: Sessions created by this factory should use this database engine
SessionLocal = sessionmaker(
    autocommit=False,  # database changes aren't automatically committed; we'll explicitly commit them
    autoflush=False,
    # SQLAlchemy won't automatically flush pending changes at certain points; we'll control when changes are sent to the database
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Base class for all SQLAlchemy ORM models.
# It allows SQLAlchemy to track our models and their database table metadata.
Base = declarative_base()

from ..models.student import Student

# Look at all the tables registered with Base, and create them in this database if they don't already exist
Base.metadata.create_all(bind=engine)
