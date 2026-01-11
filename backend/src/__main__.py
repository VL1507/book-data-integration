import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI(title="Book API", description="API для работы с книгами")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


# @app.get("/books/{book_id}", response_model=Book)
# async def get_book(book_id: int):
#     """Получить информацию о книге по её ID"""
#     book = next((book for book in books_db if book.id == book_id), None)
#     if book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book


# @app.get("/books/", response_model=List[Book])
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


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}


@app.get("/ping")
async def ping_pong():
    return {"message": "pong."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
