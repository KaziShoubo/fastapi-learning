## Day 7 — FastAPI Dependency Injection

### Goals

- Understand Dependency Injection
- Understand FastAPI's `Depends()`
- Create custom dependencies
- Inject dependencies into endpoints
- Understand database session dependencies
- Understand `yield` and dependency cleanup
- Understand dependency chaining
- Understand how one dependency can depend on another

---

### What is Dependency Injection?

Dependency Injection means that instead of a function creating something it needs itself, the required object or value is provided to it.

In FastAPI, dependencies are commonly provided using:

```python
Depends()