from repository.book import BookRepository
from schema.book import BookForListSchema


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.__book_repository = book_repository

    async def get_book_by_publication_id(self, publication_id: str):
        result = await self.__book_repository.get_book_by_pu(
            publication_id=publication_id
        )
        if result is None:
            return None
        book = ...
        return book

    async def get_books(
        self,
        limit: int = 100,
        offset: int = 0,
        genre: str | None = None,
        author: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
    ) -> list[BookForListSchema]:
        result = await self.__book_repository.get_books()
        books: list[BookForListSchema] = []
        return books
