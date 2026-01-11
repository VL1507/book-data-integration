from fastapi import APIRouter

from . import book

api_router = APIRouter()

api_router.include_router(book.router)
