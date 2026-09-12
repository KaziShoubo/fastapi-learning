# Day 09 — Authentication & Authorization

## Goals

- Understand Authentication vs Authorization
- Hash passwords securely
- Implement user registration and login
- Use OAuth2 Bearer authentication
- Create and validate JWT access tokens
- Protect FastAPI endpoints
- Implement role-based authorization
- Understand `401`, `403`, and `409`
- Use FastAPI dependencies for authentication

---

## Topics Covered

### 1. Authentication vs Authorization

**Authentication** answers:

> Who are you?

**Authorization** answers:

> What are you allowed to do?

### What I have done
 - Authentication vs Authorization
 - Password hashing
 - Password verification
 - User registration
 - OAuth2 Bearer authentication
 - OAuth2PasswordRequestForm
 - JWT access tokens
 - JWT payload
 - JWT expiration
 - JWT decoding
 - Current user dependency
 - Database-backed authentication
 - Protected endpoints
 - Role-based authorization
 - Admin-only endpoint
 - Dependency chains
 - 401 vs 403
 - 409 Conflict
 - JWT error handling
 - Swagger authentication testing


### WHat Have I tested
- Register normal user       
- Register admin user        
- Login with correct password 
- Login with wrong password   → 401 
- Duplicate username          → 409 
- Authorize through Swagger   
- /protected with JWT         → 200 
- Student → /admin            → 403 
- Admin → /admin              → 200 
- Invalid JWT handling        → 401 handling implemented 

