from sqlalchemy import select, func
from sqlalchemy.orm import aliased
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


class BookRepository:
    def __init__(self, db_session: AsyncSession):
        self.__db_session = db_session

    async def get_book_by_publication_id(self, publication_id: int):
        pass

    async def get_books(
        self,
        limit: int = 100,
        offset: int = 0,
        genre: str | None = None,
        author: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
    ):
        pub_cte = (
            select(
                Publication.id.label("publication_id"),
                Publication.name.label("title"),
                func.aggregate_strings(Authors.name, ",").label("authors"),
            )
            .join(
                PublicationAuthors, PublicationAuthors.publication_id == Publication.id
            )
            .join(Authors, Authors.id == PublicationAuthors.authors_id)
            .group_by(Publication.id, Publication.name)
            .cte("pub_cte")
        )

        stmt = (
            select(
                pub_cte.c.publication_id,
                pub_cte.c.title,
                pub_cte.c.authors,
                PublicationSite.image_url,
                Characteristics.year,
                func.aggregate_strings(Genre.genre, ",").label("genres"),
            )
            .join(
                PublicationSite,
                PublicationSite.publication_id == pub_cte.c.publication_id,
            )
            .join(
                Characteristics,
                Characteristics.publication_site_id == PublicationSite.id,
            )
            .join(
                CharacteristicsGenre,
                CharacteristicsGenre.characteristic_id
                == Characteristics.publication_site_id,
            )
            .join(Genre, Genre.id == CharacteristicsGenre.genre_id)
            .group_by(
                pub_cte.c.publication_id,
                pub_cte.c.title,
                pub_cte.c.authors,
                PublicationSite.image_url,
                Characteristics.year,
            )
            .limit(limit=limit)
            .offset(offset=offset)
        )

        result = await self.__db_session.execute(statement=stmt)

        books = list(result.all())

        return books
