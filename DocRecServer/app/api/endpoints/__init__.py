"""
Модуль импорта маршрутов API.
"""
from fastapi import APIRouter

from app.api.endpoints import (
    ping, user, pdf_files
)


api_router = APIRouter(prefix='/api')

api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(pdf_files.router, prefix="/files", tags=["files"])
