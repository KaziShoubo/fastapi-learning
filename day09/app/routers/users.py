from fastapi import APIRouter, Depends, HTTPException
from ..schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from ..database.database import get_db
from pwdlib import PasswordHash
from ..models.user import User
from sqlalchemy import select
import jwt
# Used to create the JWT expiration time.
from datetime import datetime, timedelta, timezone
from .. import config
# Standard FastAPI OAuth2 password form.
from fastapi.security import OAuth2PasswordRequestForm

# APIRouter groups our user-related endpoints.
router = APIRouter()

# Create the password hashing object once.
#
# recommended() selects a recommended secure password hashing
# configuration supported by pwdlib.
password_hash = PasswordHash.recommended()


@router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
        Register a new user.

        Flow:
            Request
              ↓
            Pydantic validation
              ↓
            Hash password
              ↓
            Check username
              ↓
            Save user to database
              ↓
            Return safe user response
        """

    # Get the plaintext password from the incoming request.
    #
    # This is only available temporarily while processing
    # the registration request.
    real_password = user_data.password

    # Hash the password before storing it.
    #
    # IMPORTANT:
    # We NEVER store the plaintext password in the database.
    hashed_password = password_hash.hash(real_password)

    # Build a query to check whether this username already exists in the database.
    # Execute the query
    # Get the existing User object if one exists.
    res = select(User).where(User.username == user_data.username)
    result = db.execute(res)
    existing_user = result.scalar_one_or_none()

    # A username should be unique.
    #
    # If it already exists, return 409 Conflict.
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="username already exist!"
        )

    user = User(
        username=user_data.username,
        password_hash=hashed_password,
        role=user_data.role
    )

    # Add the new User object to the current database session.
    db.add(user)

    # Permanently save the pending change to the database.
    db.commit()

    # Refresh the object so SQLAlchemy loads database-generated
    # values such as the new ID.
    db.refresh(user)

    # UserResponse controls what information is returned.
    #
    # Because UserResponse does not contain password_hash,
    # the password hash is not returned to the client.
    return user


@router.post("/login")
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    """
    Authenticate a user and create a JWT access token.

    Flow:
        username + password
              ↓
        find user
              ↓
        verify password
              ↓
        create JWT
              ↓
        return access token
    """

    res = select(User).where(User.username == login_data.username)
    result = db.execute(res)
    existing_user = result.scalar_one_or_none()

    # If the username doesn't exist, authentication fails.
    #
    # We deliberately use the same error message for unknown users
    # and incorrect passwords.
    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    # Compare the plaintext password supplied during login
    # with the password hash stored in the database.
    #
    # pwdlib handles the salt and hashing algorithm internally.
    check_password = password_hash.verify(login_data.password, existing_user.password_hash)

    if not check_password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    # Create an expiration time for the JWT.
    #
    # Here the token is valid for 30 minutes.
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    # Create the JWT.
    #
    # jwt.encode() receives:
    #
    # 1. payload
    # 2. secret key
    # 3. signing algorithm
    access_token = jwt.encode(
        {
            # The JWT identifies the user.
            "username": existing_user.username,

            # The role can later be used for authorization.
            "role": existing_user.role,

            # JWT automatically checks this expiration claim
            # when the token is decoded.
            "exp": expire
        },

        # Secret key used to sign the JWT.
        config.SECRET_KEY,

        # Algorithm used to sign the token.
        algorithm="HS256"
    )

    # Send the JWT back to the client.
    #
    # The client will later send:
    #
    # Authorization: Bearer <access_token>
    return {
        "access_token": access_token,
        # Tells the client which authentication scheme
        # should be used when sending the token.
        "token_type": "bearer"
    }
