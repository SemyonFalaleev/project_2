from fastapi import APIRouter, Depends
from src.handlers.article.article_create import router as create_router
from src.handlers.article.article_delete import router as delete_router
from src.handlers.article.article_get import router as get_router
from src.handlers.article.article_get_all import router as get_all_router
from src.handlers.article.article_update import router as update_router

router = APIRouter(prefix="/article", tags=["Article"])

router.include_router(create_router)
router.include_router(delete_router)
router.include_router(get_router)
router.include_router(get_all_router)
router.include_router(update_router)
