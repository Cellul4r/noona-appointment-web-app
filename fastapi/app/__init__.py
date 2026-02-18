# fastapi/app/__init__.py
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.config import settings
from app.db import Base, engine
from app.routers import auth, phonebook, event_router
from app.env_detector import should_auto_create_tables
from app.middlewares.jwt_csrf_middleware import JWTAndCSRFMiddleware

from app.models import *

import logging
import os
from fastapi.responses import JSONResponse
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from jose import jwt

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("app")

# Detect if running on Vercel (Vercel sets VERCEL=1 automatically)
api_prefix = "/api" if os.getenv("VERCEL") else ""
logger.info(f"Running with api_prefix: '{api_prefix}' (VERCEL={os.getenv('VERCEL')})")

# initialize fastapi app
fastapi_app = FastAPI(
    title="FastAPI Backend",
    debug=settings.debug,
    docs_url=f"{api_prefix}/docs",
    redoc_url=f"{api_prefix}/redoc",
    openapi_url=f"{api_prefix}/openapi.json",
)

fastapi_app.logger = logger

# add middlewares
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# fastapi_app.add_middleware(JWTAndCSRFMiddleware)

# config settings of fastapi app
fastapi_app.state.settings = settings

# Auto-detect environment and conditionally create tables
try:
    if should_auto_create_tables():
        logger.info("Auto-creating database tables (Docker)")
        Base.metadata.create_all(bind=engine)
    else:
        logger.info("Skipping table creation (Vercel/Local)")
except Exception as e:
    logger.error(f"Error during table creation: {e}")
    # Don't fail the app if table creation fails

# set all router api
fastapi_app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Auth"])
fastapi_app.include_router(
    phonebook.router, prefix=f"{api_prefix}/lab10", tags=["Phonebook"]
)
fastapi_app.include_router(event_router.router, prefix=api_prefix)


# exception handler
@fastapi_app.exception_handler(JWTError)
async def jwt_error_handler(request: Request, exc: JWTError):
    fastapi_app.logger.error(f"JWT Error: {exc}")
    return JSONResponse(status_code=401, content={"error": "Invalid token"})


@fastapi_app.exception_handler(ExpiredSignatureError)
async def jwt_expired_error_handler(request: Request, exc: ExpiredSignatureError):
    fastapi_app.logger.error(f"JWT Expired Token Error: {exc}")
    return JSONResponse(status_code=401, content={"error": "Token expired"})


fastapi_app.logger.info(
    f"Starting FastAPI app with DATABASE_URL: {settings.database_url}"
)
fastapi_app.logger.debug(f"Allowed origins: {settings.allowed_origins}")

add_pagination(fastapi_app)