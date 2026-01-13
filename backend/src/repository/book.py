from sqlalchemy import and_, distinct, exists, func, label, select, text
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
        #         stmt = select(
        #             text(f"""SELECT
        # p.id,
        # p.name,
        # GROUP_CONCAT(DISTINCT a.name),
        # GROUP_CONCAT(DISTINCT ann.description),
        # GROUP_CONCAT(DISTINCT l.lang),
        # ps.price,
        # ps.image_url,
        # s.site,
        # s.url,
        # it.name,
        # ct.name,
        # GROUP_CONCAT(DISTINCT g.genre),
        # c.year,
        # c.page_count,
        # c.dim_x,
        # c.dim_y,
        # c.dim_z
        # FROM PublicationSite ps
        # LEFT JOIN Publication p ON p.id = ps.publication_id
        # LEFT OUTER JOIN ISBN i ON i.publication_id = p.id
        # LEFT JOIN PublishingHouses ph ON ph.id = i.publisher_id
        # LEFT OUTER JOIN PublicationAuthors pa ON pa.publication_id = p.id
        # LEFT JOIN Authors a ON a.id = pa.authors_id
        # LEFT OUTER JOIN Annotation ann ON ann.publication_site_id = ps.id
        # LEFT JOIN Language l ON l.id = ann.lang_id
        # LEFT JOIN Sites s ON s.id = ps.site_id
        # LEFT JOIN Characteristics c ON c.publication_site_id = ps.id
        # LEFT JOIN IllustrationTypes it ON it.id = c.illustration_id
        # LEFT JOIN CoveragesTypes ct ON ct.id = c.cover_id
        # LEFT OUTER JOIN CharacteristicsGenre cg ON cg.characteristic_id = c.publication_site_id
        # LEFT JOIN Genre g ON g.id = cg.genre_id
        # WHERE p.id = {publication_id}
        # GROUP BY ps.id
        # """)
        #         )
        stmt = (
            select(
                Publication.id.label("publication_id"),
                Publication.name.label("title"),
                func.aggregate_strings(Authors.name.distinct(), separator=",").label(
                    "authors"
                ),
                Characteristics.year,
                func.aggregate_strings(Genre.genre.distinct(), separator=",").label(
                    "genres"
                ),
                func.aggregate_strings(
                    distinct(Annotation.description), separator=","
                ).label("annotations"),
                func.aggregate_strings(distinct(Language.lang), separator=",").label(
                    "languages"
                ),
                PublicationSite.price,
                PublicationSite.image_url,
                Sites.site,
                Sites.url,
                IllustrationTypes.name.label("illustration_type"),
                CoveragesTypes.name.label("cover_type"),
                Characteristics.page_count,
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
            .outerjoin(ISBN, ISBN.publication_id == Publication.id)
            .join(
                PublishingHouses, PublishingHouses.id == ISBN.publisher_id, isouter=True
            )
            .outerjoin(
                PublicationAuthors,
                PublicationAuthors.publication_id == Publication.id,
            )
            .join(Authors, Authors.id == PublicationAuthors.authors_id, isouter=True)
            .outerjoin(
                Annotation,
                Annotation.publication_site_id == PublicationSite.id,
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
            .outerjoin(
                CharacteristicsGenre,
                CharacteristicsGenre.characteristic_id
                == Characteristics.publication_site_id,
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
