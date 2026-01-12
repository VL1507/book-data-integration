from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel


router = APIRouter(prefix="/books")


@router.get("/{isbn:str}")
async def get_book_by_isbn(isbn: str):
    print(isbn)
    return isbn


@router.get("/")
async def get_books():
    print(get_books)
    return


# @app.get("/{book_id}", response_model=Book)
# async def get_book(book_id: int):
#     """Получить информацию о книге по её ID"""
#     book = next((book for book in books_db if book.id == book_id), None)
#     if book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book


# @app.get("/", response_model=List[Book])
# async def get_books(
#     genre: Optional[str] = Query(None, description="Фильтр по жанру"),
#     author: Optional[str] = Query(None, description="Фильтр по автору"),
#     year_from: Optional[int] = Query(None, description="Год от", ge=1000, le=2100),
#     year_to: Optional[int] = Query(None, description="Год до", ge=1000, le=2100),
#     limit: int = Query(10, description="Лимит результатов", ge=1, le=100),
#     offset: int = Query(0, description="Смещение", ge=0),
# ):
#     """Получить список книг с фильтрацией и пагинацией"""
#     filtered_books = books_db.copy()

#     if genre:
#         filtered_books = [
#             book for book in filtered_books if genre.lower() in book.genre.lower()
#         ]

#     if author:
#         filtered_books = [
#             book for book in filtered_books if author.lower() in book.author.lower()
#         ]

#     if year_from:
#         filtered_books = [book for book in filtered_books if book.year >= year_from]

#     if year_to:
#         filtered_books = [book for book in filtered_books if book.year <= year_to]

#     start_index = offset
#     end_index = offset + limit
#     paginated_books = filtered_books[start_index:end_index]

#     return paginated_books
