from sqlalchemy import and_, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

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
        title: str | None = None,
        genre: str | None = None,
        author: str | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
    ):
        stmt = (
            select(
                Publication.id,
                Publication.name,
                func.min(PublicationSite.image_url).label("image_url"),
                func.aggregate_strings(
                    Characteristics.year.distinct(), separator=","
                ).label("years"),
                func.aggregate_strings(Authors.name.distinct(), separator=",").label(
                    "authors"
                ),
                func.coalesce(
                    func.aggregate_strings(Genre.genre.distinct(), separator=",").label(
                        "genres"
                    ),
                    "",
                ),
            )
            .outerjoin(
                PublicationAuthors, PublicationAuthors.publication_id == Publication.id
            )
            .outerjoin(Authors, Authors.id == PublicationAuthors.authors_id)
            .outerjoin(
                PublicationSite, PublicationSite.publication_id == Publication.id
            )
            .outerjoin(
                Characteristics,
                Characteristics.publication_site_id == PublicationSite.id,
            )
            .outerjoin(
                CharacteristicsGenre,
                CharacteristicsGenre.characteristic_id
                == Characteristics.publication_site_id,
            )
            .outerjoin(Genre, Genre.id == CharacteristicsGenre.genre_id)
        )

        if author:
            author_exists = (
                select(PublicationAuthors.publication_id)
                .join(Authors, Authors.id == PublicationAuthors.authors_id)
                .where(
                    and_(
                        Authors.name.ilike(f"%{author}%"),
                        PublicationAuthors.publication_id == Publication.id,
                    )
                )
                .exists()
            )
            stmt = stmt.where(author_exists)

        if title:
            stmt = stmt.where(Publication.name.ilike(f"%{title}%"))

        if genre:
            genre_exists = (
                select(CharacteristicsGenre.characteristic_id)
                .join(
                    Characteristics,
                    Characteristics.publication_site_id
                    == CharacteristicsGenre.characteristic_id,
                )
                .join(Genre, Genre.id == CharacteristicsGenre.genre_id)
                .where(
                    and_(
                        Genre.genre.ilike(f"%{genre}%"),
                        Characteristics.publication_site_id == PublicationSite.id,
                        PublicationSite.publication_id == Publication.id,
                    )
                )
                .exists()
            )
            stmt = stmt.where(genre_exists)

        if year_from is not None or year_to is not None:
            year_exists_stmt = (
                select(Characteristics.publication_site_id)
                .join(
                    PublicationSite,
                    PublicationSite.id == Characteristics.publication_site_id,
                )
                .where(PublicationSite.publication_id == Publication.id)
            )

            if year_from is not None:
                year_exists_stmt = year_exists_stmt.where(
                    Characteristics.year >= year_from
                )
            if year_to is not None:
                year_exists_stmt = year_exists_stmt.where(
                    Characteristics.year <= year_to
                )

            year_exists = year_exists_stmt.exists()
            stmt = stmt.where(year_exists)

        stmt = (
            stmt.limit(limit=limit)
            .offset(offset=offset)
            .group_by(Publication.id)
            .order_by(Publication.id)
        )

        result = await self.__db_session.execute(statement=stmt)

        books = list(result.all())

        return books
