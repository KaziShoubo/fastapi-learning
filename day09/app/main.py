from fastapi import FastAPI, Depends
from .routers.users import router
from .dependencies import get_current_user, get_admin_user

# Create the FastAPI application instance.
app = FastAPI()

# Register all routes from the users router.
#
# Without this, the endpoints inside users.py
# would not be connected to this FastAPI application.
app.include_router(router)


@app.get("/protected")
def protected(current_user=Depends(get_current_user)):

    """
    Example authenticated endpoint.

    Any user with a valid JWT can access this endpoint.
    """

    # current_user is automatically provided by FastAPI.
    #
    # FastAPI executes:
    # get_current_user()
    #
    # and injects the returned User object here.
    return current_user


@app.get("/admin")
def admin(admin_user=Depends(get_admin_user)):

    """
    Example authorization-protected endpoint.

    The user must:
        1. Have a valid JWT.
        2. Exist in the database.
        3. Have role = "admin".
    """
    # admin_user is returned by get_admin_user()
    # only if the role check succeeds.
    return {
        "message": "Welcome Admin",
        "user": admin_user.username
    }
