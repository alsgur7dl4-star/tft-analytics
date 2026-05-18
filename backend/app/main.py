from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, auth, health, recommendations, tft
from app.core.config import settings
from app.core.exception_handlers import app_exception_handler, validation_exception_handler
from app.core.exceptions import AppException


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(tft.router)
    app.include_router(recommendations.router)
    app.include_router(admin.router)
    return app


app = create_app()

