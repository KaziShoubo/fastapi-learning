from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .database.database import get_db
import jwt
from sqlalchemy import select
from .models.user import User
# config contains our SECRET_KEY used to sign/verify JWTs
from . import config

# OAuth2PasswordBearer tells FastAPI that protected endpoints
# expect a token in the HTTP Authorization header:
#
# Authorization: Bearer <JWT>
#
# tokenUrl="login" tells FastAPI where clients can obtain the token.
# It is also used by Swagger/OpenAPI to build the Authorize interface.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
     Authentication dependency.

    Its job is to:
    1. Get the JWT token from the request.
    2. Decode and validate the JWT.
    3. Extract the username from the JWT.
    4. Find that user in the database.
    5. Return the database User object.
    """
    try:
        # jwt.decode() verifies the JWT signature using SECRET_KEY
        # and decodes the token payload.
        #
        # The algorithms argument tells PyJWT which signing algorithm
        # is allowed for this token.
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.InvalidTokenError:
        # If the JWT is invalid, malformed, expired, or cannot be
        # successfully validated, authentication fails.
        #
        # 401 means the client has not provided valid authentication
        # credentials.
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    # Extract the username that we placed inside the JWT
    # when the user logged in.

    username = payload["username"]
    # Build a SQLAlchemy query to find the User whose username
    # matches the username from the JWT.
    #
    # IMPORTANT:
    # This line only CREATES the query.
    # It does not execute the query yet.
    name = select(User).where(User.username == username)

    # Execute the query against the database.
    result = db.execute(name)

    # Extract the User object from the query result.
    #
    # scalar_one_or_none() means:
    #     one matching user → return User object
    #     no matching user  → return None
    user = result.scalar_one_or_none()

    # A JWT might be valid but the user could have been deleted
    # from the database after the token was created.
    #
    # Therefore, we also make sure the user actually exists.
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    # Return the actual database User object.
    #
    # FastAPI can now inject this User into other dependencies
    # or protected endpoints.
    return user


def get_admin_user(current_user=Depends(get_current_user)):
    """
    Authorization dependency.

    Authentication asks:
        "Who are you?"

    Authorization asks:
        "Are you allowed to perform this action?"

    This function checks whether the authenticated user
    has the admin role.
    """

    # get_current_user() runs first because it is a dependency.
    #
    # current_user is therefore the actual User object returned
    # by get_current_user().
    if current_user.role != "admin":

        # 403 means:
        # "I know who you are, but you are not allowed to do this."
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    # The user is authenticated AND has the required role.
    return current_user
