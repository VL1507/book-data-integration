# from app.infrastructure.database.models import User

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class BookRepository:
    db_session: AsyncSession

    async def get_book_by_isbn(self, isbn: str):
        pass
