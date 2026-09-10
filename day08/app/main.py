from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI()


@app.get("/error-test")
def error_test():
    raise HTTPException(  # We use raise to immediately stop the endpoint execution and signal to FastAPI that an HTTP error response should be returned
        status_code=400,
        detail="Something is wrong with the request"
    )


@app.get("/age-check/{age}")
def age_check(age: int):
    if age >= 18:
        return {"message": "Access granted"}

    raise HTTPException(
        status_code=400,
        detail="Student should be above 18 years old"
    )


class StudentNotFoundException(Exception):
    pass


# An async function can pause while waiting for something (for example, a database query) allowing the server to work on other requests during that wait.
# request = information about the incoming HTTP request
# exc = the actual exception that was raised
@app.exception_handler(StudentNotFoundException)
async def student_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Student not found",
            "status_code": 404
        }
    )


@app.get("/student-error")
def student_error():
    raise StudentNotFoundException()


# Middleware sits between the incoming request and your endpoint, and can also process the response before it goes back to the client
# request: Contains information about the incoming request.
# call_next: Continue processing the request and call the next part of the application.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    print(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)  # Continue processing the request through the application, including executing the endpoint, and asynchronously wait for the response.
    print(f"Response: {response.status_code}")
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Time: {elapsed:.4f} seconds")
    return response
