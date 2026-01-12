from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    ISBN,
    AdditionalCharacteristics,
    Annotation,
    Authors,
    Characteristics,
    CharacteristicsAdditional,
    CharacteristicsGenre,
    CoveragesTypes,
    Genre,
    IllustrationTypes,
    Language,
    Publication,
    PublicationAuthors,
    PublicationSite,
    PublishingHouses,
    Recension,
    Sites,
)


@dataclass
class BookRepository:
    db_session: AsyncSession

    async def get_book_by_isbn(self, isbn: str):
        pass
