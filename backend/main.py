import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from books_data import Book, books_db

app = FastAPI(title="Book API", description="API для работы с книгами")

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173"
    ],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Создаем папку для статических файлов если её нет
# os.makedirs("static/book_covers", exist_ok=True)

# Монтируем папку со статическими файлами
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Book API is running"}


# Ручка 1: Получение информации о конкретной книге по ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Получить информацию о книге по её ID"""
    book = next((book for book in books_db if book.id == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# Ручка 2: Получение обложки книги
@app.get("/books/{book_id}/cover")
async def get_book_cover(book_id: int):
    """Получить обложку книги по ID книги"""
    book = next((book for book in books_db if book.id == book_id), None)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    image_path = f"static/book_covers/{book.image_filename}"

    # Проверяем существует ли файл
    if not os.path.exists(image_path):
        # Можно вернуть заглушку или ошибку
        raise HTTPException(status_code=404, detail="Book cover not found")

    return FileResponse(image_path)


# Ручка 3: Получение списка книг с фильтрацией и пагинацией
@app.get("/books/", response_model=List[Book])
async def get_books(
    genre: Optional[str] = Query(None, description="Фильтр по жанру"),
    author: Optional[str] = Query(None, description="Фильтр по автору"),
    year_from: Optional[int] = Query(None, description="Год от", ge=1000, le=2100),
    year_to: Optional[int] = Query(None, description="Год до", ge=1000, le=2100),
    limit: Optional[int] = Query(10, description="Лимит результатов", ge=1, le=100),
    offset: Optional[int] = Query(0, description="Смещение", ge=0),
):
    """Получить список книг с фильтрацией и пагинацией"""
    filtered_books = books_db.copy()

    # Применяем фильтры
    if genre:
        filtered_books = [
            book for book in filtered_books if genre.lower() in book.genre.lower()
        ]

    if author:
        filtered_books = [
            book for book in filtered_books if author.lower() in book.author.lower()
        ]

    if year_from:
        filtered_books = [book for book in filtered_books if book.year >= year_from]

    if year_to:
        filtered_books = [book for book in filtered_books if book.year <= year_to]

    # Применяем пагинацию
    start_index = offset
    end_index = offset + limit
    paginated_books = filtered_books[start_index:end_index]

    return paginated_books


# Добавляем эндпоинт для проверки здоровья
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
