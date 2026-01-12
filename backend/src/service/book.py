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
        result = await self.__book_repository.get_books(
            limit=limit,
            offset=offset,
            genre=genre,
            author=author,
            year_from=year_from,
            year_to=year_to,
        )
        books = [
            BookForListSchema(
                publication_id=row[0],
                title=row[1],
                authors=row[3].split(","),
                image_url=row[4],
                genres=row[5].split(","),
            )
            for row in result
        ]
        return books
