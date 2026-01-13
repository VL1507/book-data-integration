from sqlalchemy import and_, exists, select, func
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

        stmt = (
            stmt.limit(limit=limit)
            .offset(offset=offset)
            .group_by(Publication.id)
            .order_by(Publication.id)
        )

        result = await self.__db_session.execute(statement=stmt)

        books = list(result.all())

        print(f"{len(books) = }")

        return books
