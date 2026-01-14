from repository.book import BookRepository
from schema.book import BookForListSchema, BookFull, PublicationSiteInfo


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.__book_repository = book_repository

    async def get_book_by_publication_id(
        self, publication_id: str
    ) -> BookFull:
        result = await self.__book_repository.get_book_by_publication_id(
            publication_id=publication_id
        )
        if len(result) == 0:
            return None

        publication_site_info: list[PublicationSiteInfo] = []

        genres: set[str] = set()
        annotation = None

        for row_mapping in result:
            psi = PublicationSiteInfo(
                year=row_mapping.get("year"),
                page_count=row_mapping.get("page_count"),
                price=row_mapping.get("price"),
                image_url=row_mapping.get("image_url"),
                site_name=row_mapping.get("site_name"),
                site_url=row_mapping.get("site_url"),
                illustration_type=row_mapping.get("illustration_type"),
                coverages_type=row_mapping.get("coverages_type"),
                dim_x=row_mapping.get("dim_x"),
                dim_y=row_mapping.get("dim_y"),
                dim_z=row_mapping.get("dim_z"),
            )
            publication_site_info.append(psi)

            genre = row_mapping.get("genres")
            if genre is not None:
                genres.update(genre.split(","))

            ann = row_mapping.get("annotations")
            if ann is not None:
                annotation = ann

        book = BookFull(
            publication_id=result[0].get("publication_id"),
            title=result[0].get("title"),
            authors=result[0].get("authors").split(","),
            genres=list(genres),
            isbn=result[0].get("isbn").split(","),
            annotation=annotation,
            publication_site_info=publication_site_info,
        )

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
    ) -> list[BookForListSchema]:
        result = await self.__book_repository.get_books(
            limit=limit,
            offset=offset,
            title=title,
            genre=genre,
            author=author,
            year_from=year_from,
            year_to=year_to,
        )
        books = [
            BookForListSchema(
                publication_id=row[0],
                title=row[1],
                image_url=row[2],
                years=list(map(int, row[3].split(","))),
                authors=row[4].split(","),
                genres=row[5].split(","),
            )
            for row in result
        ]

        return books
