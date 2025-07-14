from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import jwt, JWTError
from src.tools.security import UNPROTECTED_ROUTES, match_path

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str, algorithm: str):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithm = algorithm

    async def dispatch(self, request: Request, call_next):
        if (request.url.path == "/" or any(
            request.url.path.startswith(prefix)
            for prefix in UNPROTECTED_ROUTES
            if prefix != "/")):
            return await call_next(request)

        token = request.cookies.get("access_token")
        
        if not token:
            return JSONResponse({"detail": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            request.state.user = {
                "user_id": payload.get("sub"),
                "role_id": payload.get("role_id")
            }

        except JWTError:
            return JSONResponse({"detail": "Invalid token"}, status_code=status.HTTP_401_UNAUTHORIZED)

        return await call_next(request)

class RBACMidleware(BaseHTTPMiddleware):

    def __init__(self, app, permission: dict):
        super().__init__(app)
        self.permission = permission

    async def dispatch(self, request: Request, call_next):
        print("Внутри RBAC")
        if (request.url.path == "/" or any(
            request.url.path.startswith(prefix)
            for prefix in UNPROTECTED_ROUTES
            if prefix != "/")): 
            return await call_next(request)
        print("ПРошли не защищенные")
        try:
            user_data = request.state.user
        except AttributeError:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                                content={"detail": "Invalid token"})
        print("Токен валидный")
        method = request.method
        path = request.url.path
        allowed_routers = self.permission.get(str(user_data.get("role_id")))
        print("path", path)
        print("allowed_routers", allowed_routers)
        for pattern, methods in allowed_routers.items():
            if match_path(path, pattern) and method in methods:
                return await call_next(request)
        
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content="Forbidden")
 