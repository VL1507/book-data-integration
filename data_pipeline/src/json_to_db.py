import json
from pathlib import Path
import shutil
import time
import sys

from sqlalchemy import select

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
    PublicationSite,
    Publication,
    Recension,
    ISBN,
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

class DataShow:
    k = 5
    def __init__(self, cnt: int):
        self.start = time.perf_counter()
        self.limit = cnt
        self.cnt = 0
        self.last = ['']*self.k
    
    def add(self, resp: str):
        self.cnt += 1
        stamp = time.perf_counter()
        self.last.append(f'Book {self.cnt}/{self.limit}: {resp}&{stamp-self.start}s')
        self.last = self.last[-self.k:]

    def clear(self):
        sys.stdout.write(f"\033[{self.k}A")
        sys.stdout.write("\033[J")
    
    def reprint(self):
        self.clear()
        self.print()

    def print(self):
        width, _ = shutil.get_terminal_size()
        parsed = [('.'*(width-len(x)+1)).join(x.split('&')) if len(x) > 0 else '.'*width for x in self.last]
        sys.stdout.write("\n".join(parsed))
        sys.stdout.flush()

@timer
def dump_to_sql(book_items: list[BookSitesCrawlerItem]) -> None:
    with Session() as session:
        publication_cache: dict[str, Publication] = {}
        authors_cache: dict[str, Authors] = {}
        language_cache: dict[str, Language] = {}
        publishing_house_cache: dict[tuple[str, str], PublishingHouses] = {}
        sites_cache: dict[tuple[str, str], Sites] = {}
        genre_cache: dict[str, Genre] = {}
        coverages_types_cache: dict[str, CoveragesTypes] = {}
        illustration_types_cache: dict[str, IllustrationTypes] = {}
        data_show = DataShow(len(book_items))
        data_show.print()
        book_i = 0
        book_success = 0
        for book_item in book_items:
            logger.debug(book_i)
            book_i += 1

            # Publication
            if book_item.books_name is None:
                data_show.add("continue - book_item.books_name is None")
                data_show.reprint()
                logger.debug("continue - book_item.books_name is None")
                continue

            publication_key = book_item.books_name
            publication = publication_cache.get(publication_key)
            if publication is None:
                publication = session.scalar(
                    select(Publication).where(Publication.name == book_item.books_name)
                )
                if publication is None:
                    publication = Publication(name=book_item.books_name)
                    session.add(publication)
                publication_cache[publication_key] = publication

            session.flush()

            # Recension
            recension = session.scalar(
                select(Recension).where(Recension.publication_id == publication.id)
            )
            if recension is None:
                if book_item.recension_link is not None:
                    recension = Recension(
                        publication_id=publication.id, link=book_item.recension_link
                    )
                    session.add(Recension)

            session.flush()

            # Authors
            if len(book_item.authors_name) == 0:
                data_show.add("continue - len(book_item.authors_name) == 0")
                data_show.reprint()
                logger.debug("continue - len(book_item.authors_name) == 0")
                continue

            for author_name in book_item.authors_name:
                author_key = author_name
                author = authors_cache.get(author_key)
                if author is None:
                    author = session.scalar(
                        select(Authors).where(Authors.name == author_name)
                    )
                    if author is None:
                        author = Authors(name=author_name)
                        session.add(author)
                    authors_cache[author_key] = author

                session.flush()

                # PublicationAuthors
                publication_authors = session.scalar(
                    select(PublicationAuthors).where(
                        PublicationAuthors.publication_id == publication.id,
                        PublicationAuthors.authors_id == author.id,
                    )
                )
                if publication_authors is None:
                    publication_authors = PublicationAuthors(
                        publication_id=publication.id, authors_id=author.id
                    )
                    session.add(publication_authors)

            session.flush()

            # Language
            if book_item.lang is None:
                # logger.debug("continue - book_item.lang is None")
                # continue
                book_item.lang = "Русский(None)"

            language_key = book_item.lang
            language = language_cache.get(language_key)
            if language is None:
                language = session.scalar(
                    select(Language).where(Language.lang == book_item.lang)
                )
                if language is None:
                    language = Language(lang=book_item.lang)
                    session.add(language)
                language_cache[language_key] = language

            session.flush()

            # PublishingHouses
            if book_item.publishing_houses_name is None:
                data_show.add("continue - book_item.publishing_houses_name is None")
                data_show.reprint()
                logger.debug("continue - book_item.publishing_houses_name is None")
                continue

            publishing_house_key = (
                book_item.publishing_houses_name,
                book_item.publishing_houses_url,
            )
            publishing_house = publishing_house_cache.get(publishing_house_key)
            if publishing_house is None:
                publishing_house = session.scalar(
                    select(PublishingHouses).where(
                        PublishingHouses.name == book_item.publishing_houses_name,
                        PublishingHouses.url == book_item.publishing_houses_url,
                    )
                )
                if publishing_house is None:
                    publishing_house = PublishingHouses(
                        name=book_item.publishing_houses_name,
                        url=book_item.publishing_houses_url,
                    )
                    session.add(publishing_house)
                publishing_house_cache[publishing_house_key] = publishing_house

            session.flush()

            # ISBN
            if len(book_item.isbn) == 0:
                data_show.add("continue - len(book_item.isbn) == 0")
                data_show.reprint()
                logger.debug("continue - len(book_item.isbn) == 0")
                continue

            for book_isbn in book_item.isbn:
                isbn = session.scalar(select(ISBN).where(ISBN.isbn == book_isbn))
                if isbn is None:
                    isbn = ISBN(
                        isbn=book_isbn,
                        publication_id=publication.id,
                        publisher_id=publishing_house.id,
                    )
                    session.add(isbn)

            session.flush()

            # Sites
            site_key = (book_item.sites_site, book_item.sites_url)
            site = sites_cache.get(site_key)
            if site is None:
                site = session.scalar(
                    select(Sites).where(
                        Sites.site == book_item.sites_site,
                        Sites.url == book_item.sites_url,
                    )
                )
                if site is None:
                    site = Sites(site=book_item.sites_site, url=book_item.sites_url)
                    session.add(site)
                sites_cache[site_key] = site

            session.flush()

            # PublicationSite
            if book_item.publication_site_price is None:
                data_show.add("continue - book_item.publication_site_price is None")
                data_show.reprint()
                logger.debug("continue - book_item.publication_site_price is None")
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
            if book_item.description is None:
                logger.debug("continue - book_item.publication_site_price is None")
                # continue
            else:
                annotation = Annotation(
                    publication_site_id=publication_site.id,
                    lang_id=language.id,
                    description=book_item.description,
                )
                session.add(annotation)

            session.flush()

            # CoveragesTypes
            if book_item.coverages_types_name is None:
                logger.debug("- book_item.coverages_types_name is None")
                # continue
                coverages_types = None
            else:
                coverages_types_key = book_item.coverages_types_name
                coverages_types = coverages_types_cache.get(coverages_types_key)
                if coverages_types is None:
                    coverages_types = session.scalar(
                        select(CoveragesTypes).where(
                            CoveragesTypes.name == book_item.coverages_types_name
                        )
                    )
                    if coverages_types is None:
                        coverages_types = CoveragesTypes(
                            name=book_item.coverages_types_name
                        )
                        session.add(coverages_types)
                    coverages_types_cache[coverages_types_key] = coverages_types

            session.flush()

            # IllustrationTypes

            if book_item.illustration_types_name is None:
                logger.debug("- book_item.illustration_types_name is None")
                # continue
                illustration_types = None
            else:
                illustration_types_key = book_item.illustration_types_name
                illustration_types = illustration_types_cache.get(
                    illustration_types_key
                )
                if illustration_types is None:
                    illustration_types = session.scalar(
                        select(IllustrationTypes).where(
                            IllustrationTypes.name == book_item.illustration_types_name
                        )
                    )
                    if illustration_types is None:
                        illustration_types = IllustrationTypes(
                            name=book_item.illustration_types_name
                        )
                        session.add(illustration_types)
                    illustration_types_cache[illustration_types_key] = (
                        illustration_types
                    )

            session.flush()

            # AdditionalCharacteristics

            # Characteristics
            if book_item.year is None:
                data_show.add("continue - book_item.year is None")
                data_show.reprint()
                logger.debug("continue - book_item.year is None")
                continue
            if book_item.page_count is None:
                data_show.add("continue - book_item.page_count is None")
                data_show.reprint()
                logger.debug("continue - book_item.page_count is None")
                continue

            characteristics = Characteristics(
                publication_site_id=publication_site.id,
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

            # Genre

            # if len(book_item.genre) == 0:
            #     logger.debug("continue - len(book_item.genre) == 0")
            #     continue

            for book_genre in book_item.genre:
                genre_key = book_genre
                genre = genre_cache.get(genre_key)
                if genre is None:
                    genre = session.scalar(
                        select(Genre).where(Genre.genre == book_genre)
                    )
                    if genre is None:
                        genre = Genre(genre=book_genre)
                        session.add(genre)
                    genre_cache[genre_key] = genre

                    session.flush()

                # CharacteristicsGenre

                characteristics_genre = CharacteristicsGenre(
                    characteristic_id=characteristics.publication_site_id,
                    genre_id=genre.id,
                )
                session.add(characteristics_genre)

            session.flush()

            # CharacteristicsAdditional

            session.flush()

            session.commit()
            book_success += 1
            data_show.add("finished - all data added")
            data_show.reprint()
        session.commit()
        data_show.clear()
        print(f"Успешно загружено {book_success} из {book_i} | {book_success / book_i * 100:.2f}%")
        logger.debug(
            f"Успешно загружено {book_success} из {book_i} | {book_success / book_i * 100:.2f}%"
        )
