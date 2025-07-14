from fastapi import APIRouter, Depends
from src.handlers.user.user_delete import router as delete_router
from src.handlers.user.user_update import router as update_router 
from src.handlers.user.user_get import router as get_router 
# from src.utils.security import check_admin

router = APIRouter(prefix="/user", tags=["User"])

router.include_router(delete_router)
router.include_router(update_router)
router.include_router(get_router)