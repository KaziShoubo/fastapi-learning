from fastapi import FastAPI

# app is the FastAPI application instance that we'll use to define our API.
app = FastAPI()


# @app.get("/") registers the function below it to handle GET requests sent to the / path.
# / represents the path, not the entire URL.
@app.get("/")
def home():
    return {"message": "Welcome to Student API!"}


@app.get("/about")
def app_details():
    return {"name": "Student API",
            "version": "1.0",
            "description": "API for managing Student information"
            }


@app.get("/students")
def student_list():
    student1 = ["Shoubo", 28, "male"]
    student2 = ["Samiha", 25, "Female"]
    student3 = ["Jubayer", 23, "Male"]
    return [
        student1,
        student2,
        student3
    ]


@app.get("/health")
def health_status():
    return {"status": "healthy"}
