from dataclasses import dataclass

from repository.book import BookRepository


@dataclass
class BookService:
    book_repository: BookRepository

    async def get_book_by_isbn(self, isbn: str):
        result = await self.book_repository.get_book_by_isbn(isbn=isbn)
        if result is None:
            return None
        book = ...
        return book
