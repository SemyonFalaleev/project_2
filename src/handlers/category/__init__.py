from fastapi import APIRouter, Depends
from src.handlers.category.category_create import router as create_router
from src.handlers.category.category_delete import router as delete_router
from src.handlers.category.category_update import router as update_router 
from src.handlers.category.category_get import router as get_router 
from src.handlers.category.category_get_all import router as get_all_router

router = APIRouter(prefix="/category", tags=["Category"])

router.include_router(create_router)
router.include_router(delete_router)
router.include_router(update_router)
router.include_router(get_router)
router.include_router(get_all_router)