from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from database.accessor import get_db_session
from repository.book import BookRepository
from service.book import BookService


async def get_book_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> BookRepository:
    return BookRepository(db_session=db_session)


async def get_book_service(
    book_repository: BookRepository = Depends(get_book_repository),
) -> BookService:
    return BookService(book_repository=book_repository)
