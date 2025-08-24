from fastapi import APIRouter, Response

router = APIRouter(tags=["Health"])


@router.get(path="/health")
def health_check():
    return Response("OK", status_code=200)
