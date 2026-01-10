import json
from pathlib import Path

from db_conn import Session


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


def load_from_json(path: Path) -> list[BookSitesCrawlerItem]:
    with open(file=path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    items = []
    for row in data:
        item = BookSitesCrawlerItem(**row)
        items.append(item)

    return items


def dump_to_sql(book_items: list[BookSitesCrawlerItem]) -> None:
    with Session() as session:
        # Кэши, чтобы отправлять меньше запросов в бд
        sites_cache: dict[tuple[str, str], Sites] = {}
        publishing_house_cache: dict[tuple[str, str], Sites] = {}
        authors_cache: dict[str, Authors] = {}
        book_cache: dict[str, Books] = {}
        coverages_types_cache: dict[str, CoveragesTypes] = {}

        for book_item in book_items:
            # Sites
            site_key = (book_item.sites_site, book_item.sites_url)
            site = sites_cache.get(site_key)
            if not site:
                site = (
                    session.query(Sites)
                    .where(
                        Sites.site == book_item.sites_site,
                        Sites.url == book_item.sites_url,
                    )
                    .first()
                )
                if not site:
                    site = Sites(site=book_item.sites_site, url=book_item.sites_url)
                    session.add(site)
                sites_cache[site_key] = site

            # PublishingHouse
            publishing_house_key = (
                book_item.publishing_houses_name,
                book_item.publishing_houses_url,
            )
            publishing_house = publishing_house_cache.get(publishing_house_key)
            if not publishing_house:
                publishing_house = (
                    session.query(PublishingHouses)
                    .where(
                        PublishingHouses.name == book_item.publishing_houses_name,
                        PublishingHouses.url == book_item.publishing_houses_url,
                    )
                    .first()
                )
                if not publishing_house:
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

                if not author:
                    author = (
                        session.query(Authors)
                        .where(Authors.name == author_name)
                        .first()
                    )
                    if not author:
                        author = Authors(name=author_name)
                        session.add(author)
                    authors_cache[author_key] = author
                authors.append(author)

            # Books
            book_key = book_item.books_name
            book = book_cache.get(book_key)
            if not book:
                book = (
                    session.query(Books)
                    .where(Books.name == book_item.books_name)
                    .first()
                )
                if not book:
                    book = Books(name=book_item.books_name)
                    session.add(book)
                book_cache[book_key] = book

            # CoveragesTypes
            coverages_types_key = book_item.coverages_types_name
            coverages_types = coverages_types_cache.get(coverages_types_key)
            if not coverages_types:
                coverages_types = (
                    session.query(CoveragesTypes)
                    .where(CoveragesTypes.name == book_item.coverages_types_name)
                    .first()
                )
                if not coverages_types:
                    coverages_types = CoveragesTypes(
                        name=book_item.coverages_types_name
                    )
                    session.add(coverages_types)
                    
                    
                    
                    

            session.flush()
            
            
            
        # session.commit()
