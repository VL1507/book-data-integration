import json
from pathlib import Path

from db_conn import Session
from wrap_timer import timer

from json_model import BookSitesCrawlerItem
from models import (
    Sites,
    AdditionalCharacteristics,
    Annotation,
    Authors,
    PublicationAuthors,
    CharacteristicsAdditional,
    PublishingHouses,
    Language,
    Characteristics,
    CharacteristicsGenre,
    CoveragesTypes,
    Genre,
    IllustrationTypes,
    Books,
    PublicationSite,
    Publication,
    Recension,
)

import logging

logger = logging.getLogger(name=__name__)


@timer
def load_from_json(path: Path) -> list[BookSitesCrawlerItem]:
    with open(file=path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    items = []
    for row in data:
        item = BookSitesCrawlerItem(**row)
        items.append(item)

    return items


@timer
def dump_to_sql(book_items: list[BookSitesCrawlerItem]) -> None:
    with Session() as session:
        sites_cache: dict[tuple[str, str], Sites] = {}
        publishing_house_cache: dict[tuple[str, str], Sites] = {}
        authors_cache: dict[str, Authors] = {}
        book_cache: dict[str, Books] = {}
        coverages_types_cache: dict[str, CoveragesTypes] = {}
        language_cache: dict[str, Language] = {}
        illustration_types_cache: dict[str, IllustrationTypes] = {}
        genre_cache: dict[str, Genre] = {}

        book_i = 0
        for book_item in book_items:
            logger.debug(book_i)
            book_i += 1
            # Sites
            site_key = (book_item.sites_site, book_item.sites_url)
            site = sites_cache.get(site_key)
            if site is None:
                site = (
                    session.query(Sites)
                    .where(
                        Sites.site == book_item.sites_site,
                        Sites.url == book_item.sites_url,
                    )
                    .first()
                )
                if site is None:
                    site = Sites(site=book_item.sites_site, url=book_item.sites_url)
                    session.add(site)
                sites_cache[site_key] = site

            # PublishingHouse
            if (
                book_item.publishing_houses_name is None
                # or book_item.publishing_houses_url is None
            ):
                logger.debug("continue - book_item.publishing_houses_name is None")
                continue
            publishing_house_key = (
                book_item.publishing_houses_name,
                book_item.publishing_houses_url,
            )
            publishing_house = publishing_house_cache.get(publishing_house_key)
            if publishing_house is None:
                publishing_house = (
                    session.query(PublishingHouses)
                    .where(
                        PublishingHouses.name == book_item.publishing_houses_name,
                        PublishingHouses.url == book_item.publishing_houses_url,
                    )
                    .first()
                )
                if publishing_house is None:
                    publishing_house = PublishingHouses(
                        name=book_item.publishing_houses_name,
                        url=book_item.publishing_houses_url,
                    )
                    session.add(publishing_house)
                publishing_house_cache[publishing_house_key] = publishing_house

            # Authors
            authors: list[Authors] = []
            for author_name in book_item.authors_name:
                author_key = author_name
                author = authors_cache.get(author_key)

                if author is None:
                    author = (
                        session.query(Authors)
                        .where(Authors.name == author_name)
                        .first()
                    )
                    if author is None:
                        author = Authors(name=author_name)
                        session.add(author)
                    authors_cache[author_key] = author
                authors.append(author)

            if len(authors) == 0:
                logger.debug("continue - len(authors) == 0")
                continue

            # Books
            if book_item.books_name is None:
                logger.debug("continue - book_item.books_name is None")
                continue
            book_key = book_item.books_name
            book = book_cache.get(book_key)
            if book is None:
                book = (
                    session.query(Books)
                    .where(Books.name == book_item.books_name)
                    .first()
                )
                if book is None:
                    book = Books(name=book_item.books_name)
                    session.add(book)
                book_cache[book_key] = book

            # CoveragesTypes

            if book_item.coverages_types_name is None:
                # logger.debug("continue - book_item.coverages_types_name is None")
                # continue
                coverages_types = None
            else:
                coverages_types_key = book_item.coverages_types_name
                coverages_types = coverages_types_cache.get(coverages_types_key)
                if coverages_types is None:
                    coverages_types = (
                        session.query(CoveragesTypes)
                        .where(CoveragesTypes.name == book_item.coverages_types_name)
                        .first()
                    )
                    if coverages_types is None:
                        coverages_types = CoveragesTypes(
                            name=book_item.coverages_types_name
                        )
                        session.add(coverages_types)

            # Language
            if book_item.lang is None:
                logger.debug("- book_item.lang is None")
                book_item.lang = "Русский"
                # continue
            language_key = book_item.lang
            language = language_cache.get(language_key)
            if language is None:
                language = (
                    session.query(Language)
                    .where(Language.lang == book_item.lang)
                    .first()
                )
                if language is None:
                    language = Language(lang=book_item.lang)
                    session.add(language)
                language_cache[language_key] = language

            # IllustrationTypes

            if book_item.illustration_types_name is None:
                # logger.debug("continue - book_item.illustration_types_name is None")
                # continue
                illustration_types = None
            else:
                illustration_types_key = book_item.illustration_types_name
                illustration_types = illustration_types_cache.get(
                    illustration_types_key
                )
                if illustration_types is None:
                    illustration_types = (
                        session.query(IllustrationTypes)
                        .where(
                            IllustrationTypes.name == book_item.illustration_types_name
                        )
                        .first()
                    )
                    if illustration_types is None:
                        illustration_types = IllustrationTypes(
                            name=book_item.illustration_types_name
                        )
                        session.add(illustration_types)
                    illustration_types_cache[illustration_types_key] = (
                        illustration_types
                    )

            # Genre
            genres: list[Genre] = []

            for genre_name in book_item.genre:
                genre_key = genre_name
                genre = genre_cache.get(genre_key)
                if genre is None:
                    genre = (
                        session.query(Genre).where(Genre.genre == genre_name).first()
                    )
                    if genre is None:
                        genre = Genre(genre=genre_name)
                        session.add(genre)
                    genre_cache[genre_key] = genre
                genres.append(genre)

            if len(genres) == 0:
                logger.debug("len(genres) == 0")
                # continue

            # AdditionalCharacteristics

            session.flush()

            # Publication
            if book.id is None:
                logger.debug("continue - book.id is None")
                continue
            if publishing_house.id is None:
                logger.debug("continue - publishing_house.id is None")
                continue
            publication = Publication(book_id=book.id, publisher_id=publishing_house.id)
            session.add(publication)

            session.flush()

            # PublicationSite
            if publication.id is None:
                logger.debug("""continue - publication.id is None""")
                continue
            if site.id is None:
                logger.debug("""continue - site.id is None""")
                continue
            if book_item.publication_site_price is None:
                logger.debug("""continue - book_item.publication_site_price is None""")
                continue

            publication_site = PublicationSite(
                publication_id=publication.id,
                site_id=site.id,
                price=book_item.publication_site_price,
                image_url=book_item.image_urls,
            )
            session.add(publication_site)

            session.flush()

            # Annotation
            if publication_site.id is None:
                logger.debug("""continue - publication_site.id""")
                continue

            if book_item.description is None:
                logger.debug("""continue - book_item.description is None""")
                # continue
            else:
                if language.id is None:
                    logger.debug("""continue - language.id is None""")
                    # continue
                else:
                    annotation = Annotation(
                        lang_id=language.id,
                        publication_site_id=publication_site.id,
                        description=book_item.description,
                    )
                    session.add(annotation)

            # Recension

            # PublicationAuthors
            if publication.id is None:
                logger.debug("""continue - publication.id is None""")
                continue
            for author in authors:
                if author.id is None:
                    continue
                publication_authors = PublicationAuthors(
                    authors_id=author.id, publication_id=publication.id
                )
                session.add(publication_authors)

            # CharacteristicsAdditional

            # Characteristics
            if publication.id is None:
                logger.debug("""continue - publication.id is None""")
                continue
            if book_item.year is None:
                logger.debug("""continue - book_item.year is None""")
                continue
            if book_item.page_count is None:
                logger.debug("""continue - book_item.page_count is None""")
                continue
            
            for isbn in book_item.isbn:
                characteristics = Characteristics(
                    publication_id=publication.id,
                    ISBN=isbn,
                    year=book_item.year,
                    page_count=book_item.page_count,
                    dim_x=book_item.dim_x,
                    dim_y=book_item.dim_y,
                    dim_z=book_item.dim_z,
                    cover_id=coverages_types.id
                    if coverages_types is not None
                    else coverages_types,
                    illustration_id=illustration_types.id
                    if illustration_types is not None
                    else illustration_types,
                )
                session.add(characteristics)

                session.flush()

                # CharacteristicsGenre
                if characteristics.id is None:
                    logger.debug(
                        """continue - characteristics.id is None"""
                    )
                    continue
                for genre in genres:
                    if genre.id is None:
                        logger.debug("""continue - genre.id is None""")
                        continue
                    characteristics_genre = CharacteristicsGenre(
                        characteristic_id=characteristics.id,
                        genre_id=genre.id,
                    )
                    session.add(characteristics_genre)

            session.flush()

        session.commit()
