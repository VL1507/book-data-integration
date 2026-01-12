from dataclasses import dataclass

from repository.book import BookRepository


@dataclass
class BookService:
    book_repository: BookRepository

    async def get_book_by_isbn(self, isbn: str):
        pass
