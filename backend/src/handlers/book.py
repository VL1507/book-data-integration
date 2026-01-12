from fastapi import APIRouter, Depends, HTTPException, Query, status

from dependency import get_book_service
from service.book import BookService

router = APIRouter(prefix="/books")


@router.get("/{isbn:str}")
async def get_book_by_isbn(
    isbn: str,
    book_service: BookService = Depends(get_book_service),
):
    print(isbn)
    book = await book_service.get_book_by_isbn(isbn=isbn)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with isbn {isbn} not found",
        )
    return book


@router.get("/")
async def get_books(
    genre: str | None = Query(None, description="Фильтр по жанру"),
    author: str | None = Query(None, description="Фильтр по автору"),
    year_from: int | None = Query(None, description="Год от", ge=1000, le=2100),
    year_to: int | None = Query(None, description="Год до", ge=1000, le=2100),
    limit: int = Query(10, description="Лимит результатов", ge=1, le=100),
    offset: int = Query(0, description="Смещение", ge=0),
    book_service: BookService = Depends(get_book_service),
):
    print(genre, author, year_from, year_to, limit, offset)

    return [genre, author, year_from, year_to, limit, offset]
