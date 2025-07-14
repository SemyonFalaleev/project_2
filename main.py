from fastapi import FastAPI
import uvicorn
from src.middlewear.protected import AuthMiddleware, RBACMidleware
from src.tools.security import parse_permission_dict
from src.handlers.user import router as user_router
from src.handlers.category import router as category_router
from src.handlers.article import router as article_router
from src.handlers.auth import router as auth_router
from decouple import config

app = FastAPI(title="blog_marcketplace")

app.add_middleware(RBACMidleware, 
                   parse_permission_dict(config("PATH_TO_PERMISSION_JSON"))
                   )

app.add_middleware(AuthMiddleware,
                   config("SECRET_KEY_JWT"),
                   config("ALGORITM_JWT"))

app.include_router(router=user_router)
app.include_router(router=category_router)
app.include_router(router=article_router)
app.include_router(router=auth_router)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)