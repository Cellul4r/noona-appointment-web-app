import logging

from fastapi import HTTPException
from app.config import settings
from jose import JWTError, jwt

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this logger to DEBUG


class JWTAndCSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        excluded_paths = ["/", "/login", "/google/auth", "/logout", "/signup"]
        logger.debug(f"Request method: {request.method}, path: {request.url.path}")
        if (
            request.method not in ["POST", "PUT", "DELETE"]
            or request.url.path in excluded_paths
        ):
            logger.debug("Skipping JWT/CSRF validation for this request")
            return await call_next(request)

        token = request.cookies.get("jwt")
        logger.debug(f"JWT cookie: {token}")
        if not token:
            logger.error("Missing JWT cookie in middleware")
            raise HTTPException(status_code=401, detail="Missing JWT cookie")

        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
            logger.debug(f"JWT payload: {payload}")
        except JWTError as e:
            logger.error(f"JWT decoding failed in middleware: {e}")
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        client_csrf = request.headers.get("X-CSRF-Token")
        logger.debug(f"Client CSRF token: {client_csrf}")
        if not client_csrf or payload.get("csrf_token") != client_csrf:
            logger.error("CSRF token mismatch in middleware")
            raise HTTPException(status_code=403, detail="CSRF token mismatch")

        response = await call_next(request)
        return response
