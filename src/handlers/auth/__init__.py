from fastapi import APIRouter
from src.handlers.auth.sign_up import router as sign_up_router
from src.handlers.auth.sign_in import router as sign_in_router
from src.handlers.auth.logout import router as logout_router
from src.handlers.auth.accepted_email import router as conf_email_router
# from src.utils.security import check_admin

router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(sign_up_router)
router.include_router(sign_in_router)
router.include_router(logout_router)
router.include_router(conf_email_router)
