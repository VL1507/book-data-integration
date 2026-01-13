from sqlalchemy import and_, distinct, func, select
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
        stmt = (
            select(
                Publication.id.label("publication_id"),
                Publication.name.label("title"),
                func.aggregate_strings(Authors.name.distinct(), separator=",").label(
                    "authors"
                ),
                func.aggregate_strings(Genre.genre.distinct(), separator=",").label(
                    "genres"
                ),
                func.aggregate_strings(
                    distinct(Annotation.description), separator=","
                ).label("annotations"),
                #
                #
                #
                Characteristics.year,
                Characteristics.page_count,
                PublicationSite.price,
                PublicationSite.image_url,
                Sites.site.label("site_name"),
                Sites.url.label("site_url"),
                IllustrationTypes.name.label("illustration_type"),
                CoveragesTypes.name.label("coverages_type"),
                func.aggregate_strings(Language.lang.distinct(), separator=",").label(
                    "languages"
                ),
                Characteristics.dim_x,
                Characteristics.dim_y,
                Characteristics.dim_z,
            )
            .select_from(PublicationSite)
            .join(
                Publication,
                Publication.id == PublicationSite.publication_id,
                isouter=True,
            )
            .join(ISBN, ISBN.publication_id == Publication.id, isouter=True)
            .join(
                PublishingHouses, PublishingHouses.id == ISBN.publisher_id, isouter=True
            )
            .join(
                PublicationAuthors,
                PublicationAuthors.publication_id == Publication.id,
                isouter=True,
            )
            .join(Authors, Authors.id == PublicationAuthors.authors_id)
            .join(
                Annotation,
                Annotation.publication_site_id == PublicationSite.id,
                isouter=True,
            )
            .join(Language, Language.id == Annotation.lang_id, isouter=True)
            .join(Sites, Sites.id == PublicationSite.site_id, isouter=True)
            .join(
                Characteristics,
                Characteristics.publication_site_id == PublicationSite.id,
                isouter=True,
            )
            .join(
                IllustrationTypes,
                IllustrationTypes.id == Characteristics.illustration_id,
                isouter=True,
            )
            .join(
                CoveragesTypes,
                CoveragesTypes.id == Characteristics.cover_id,
                isouter=True,
            )
            .join(
                CharacteristicsGenre,
                CharacteristicsGenre.characteristic_id
                == Characteristics.publication_site_id,
                isouter=True,
            )
            .join(Genre, Genre.id == CharacteristicsGenre.genre_id, isouter=True)
            .where(Publication.id == publication_id)
            .group_by(PublicationSite.id)
        )
        result = await self.__db_session.execute(statement=stmt)

        book = list(result.mappings().all())

        print(book)

        return book

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
