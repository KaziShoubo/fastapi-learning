from fastapi import Depends, APIRouter
from ..dependencies import get_message, get_app_name

router = APIRouter()


# telling fastapi that Before running this endpoint, get the value from get_message() and provide it as message
@router.get("/test")
def test_dependency(message: str = Depends(get_message)):
    return {
        "message": message
    }


@router.get("/app-info")
def test_dependency_name(message: str = Depends(get_app_name)):
    return {
        "app_name": message
    }
