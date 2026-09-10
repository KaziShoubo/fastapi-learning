## Day 8 — Error Handling, Middleware & Logging

###  Goals

- Understand HTTP errors and status codes
- Use `HTTPException`
- Create custom exceptions
- Create custom exception handlers
- Understand middleware
- Log incoming requests
- Log response status codes
- Measure request processing time
- Understand basic `async def` and `await`

---

###  HTTPException

FastAPI provides `HTTPException` for returning HTTP error responses.

Example:

```python
raise HTTPException(
    status_code=400,
    detail="Something is wrong with the request"
)