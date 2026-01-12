from fastapi import APIRouter

from . import book, health

api_router = APIRouter()

api_router.include_router(book.router)
api_router.include_router(health.router)
