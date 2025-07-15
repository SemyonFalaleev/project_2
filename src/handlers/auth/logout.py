from fastapi import APIRouter, status
from fastapi.responses import Response

router = APIRouter()


@router.post("/logout")
async def logout_user():
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(key="access_token", path="/")
    return response
