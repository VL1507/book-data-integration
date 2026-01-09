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
        # Кэши для справочников, чтобы не делать запросы на каждую книгу
        sites_cache: dict[str, Sites] = {}
        authors_cache: dict[str, Authors] = {}
        publishers_cache: dict[str, PublishingHouses] = {}
        languages_cache: dict[str, Language] = {}
        coverage_cache: dict[str, CoveragesTypes] = {}
        illustration_cache: dict[str, IllustrationTypes] = {}
        genre_cache: dict[str, Genre] = {}
        additional_cache: dict[str, AdditionalCharacteristics] = {}

        for item in book_items:
            # 1. Site (Sites)
            site_key = (item.sites_site, item.sites_url)
            site = sites_cache.get(site_key)
            if not site:
                site = (
                    session.query(Sites)
                    .filter_by(site=item.sites_site, url=item.sites_url)
                    .first()
                )
                if not site:
                    site = Sites(site=item.sites_site, url=item.sites_url)
                    session.add(site)
                sites_cache[site_key] = site

            # 2. PublishingHouse
            publisher = None
            if item.publishing_houses_name:
                publisher_key = (
                    item.publishing_houses_name,
                    item.publishing_houses_url or "",
                )
                publisher = publishers_cache.get(publisher_key)
                if not publisher:
                    publisher = (
                        session.query(PublishingHouses)
                        .filter_by(
                            name=item.publishing_houses_name,
                            url=item.publishing_houses_url,
                        )
                        .first()
                    )
                    if not publisher:
                        publisher = PublishingHouses(
                            name=item.publishing_houses_name,
                            url=item.publishing_houses_url,
                        )
                        session.add(publisher)
                    publishers_cache[publisher_key] = publisher

            # 3. Book (Books)
            book = None
            if item.books_name:
                book = session.query(Books).filter_by(name=item.books_name).first()
                if not book:
                    book = Books(name=item.books_name)
                    session.add(book)

            # 4. Publication (основная связь книга + издательство)
            publication = None
            if book and publisher:
                publication = (
                    session.query(Publication)
                    .join(Books)
                    .join(PublishingHouses)
                    .filter(Books.id == book.id, PublishingHouses.id == publisher.id)
                    .first()
                )
                if not publication:
                    publication = Publication(
                        book_id=book.id, publisher_id=publisher.id
                    )
                    session.add(publication)

            # Если нет издательства, но есть книга — создаём Publication без publisher
            if not publication and book:
                publication = Publication(book=book, publisher=None)
                session.add(publication)

            # Фиксим сессию, чтобы получить ID после возможного flush
            session.flush()

            if not publication:
                # Если вообще ничего не удалось создать — пропускаем запись
                continue

            # 5. Authors
            authors = []
            for author_name in item.authors_name:
                if not author_name:
                    continue
                author = authors_cache.get(author_name)
                if not author:
                    author = session.query(Authors).filter_by(name=author_name).first()
                    if not author:
                        author = Authors(name=author_name)
                        session.add(author)
                    authors_cache[author_name] = author
                authors.append(author)

            # Связываем авторов с публикацией через ассоциативную таблицу
            for author in authors:
                assoc = (
                    session.query(PublicationAuthors)
                    .filter_by(publication_id=publication.id, authors_id=author.id)
                    .first()
                )
                if not assoc:
                    session.add(
                        PublicationAuthors(
                            publication_id=publication.id, authors_id=author.id
                        )
                    )

            # 6. Characteristics (наследуется от Publication)
            characteristics = (
                session.query(Characteristics)
                .filter_by(publication_id=publication.id)
                .first()
            )
            if not characteristics:
                characteristics = Characteristics(
                    publication_id=publication.id,
                    ISBN=", ".join(item.isbn)
                    if item.isbn
                    else None,  # или можно хранить в отдельной таблице
                    year=item.year,
                    page_count=item.page_count,
                    dim_x=item.dim_x,
                    dim_y=item.dim_y,
                    dim_z=item.dim_z,
                )
                session.add(characteristics)

            # Cover type
            if item.coverages_types_name:
                cover = coverage_cache.get(item.coverages_types_name)
                if not cover:
                    cover = (
                        session.query(CoveragesTypes)
                        .filter_by(name=item.coverages_types_name)
                        .first()
                    )
                    if not cover:
                        cover = CoveragesTypes(name=item.coverages_types_name)
                        session.add(cover)
                    coverage_cache[item.coverages_types_name] = cover
                characteristics.cover = cover

            # Illustration type
            if item.illustration_types_name:
                illus = illustration_cache.get(item.illustration_types_name)
                if not illus:
                    illus = (
                        session.query(IllustrationTypes)
                        .filter_by(name=item.illustration_types_name)
                        .first()
                    )
                    if not illus:
                        illus = IllustrationTypes(name=item.illustration_types_name)
                        session.add(illus)
                    illustration_cache[item.illustration_types_name] = illus
                characteristics.illustration = illus

            # Genres
            for genre_name in item.genre:
                if not genre_name:
                    continue
                genre_obj = genre_cache.get(genre_name)
                if not genre_obj:
                    genre_obj = session.query(Genre).filter_by(genre=genre_name).first()
                    if not genre_obj:
                        genre_obj = Genre(genre=genre_name)
                        session.add(genre_obj)
                    genre_cache[genre_name] = genre_obj

                # Связь через CharacteristicsGenre
                assoc = (
                    session.query(CharacteristicsGenre)
                    .filter_by(characteristic_id=publication.id, genre_id=genre_obj.id)
                    .first()
                )
                if not assoc:
                    session.add(
                        CharacteristicsGenre(
                            characteristic_id=publication.id, genre_id=genre_obj.id
                        )
                    )

            # 7. PublicationSite (цена, ссылка на сайт, изображение)
            pub_site = (
                session.query(PublicationSite)
                .filter_by(publication_id=publication.id, site_id=site.id)
                .first()
            )

            if not pub_site:
                pub_site = PublicationSite(
                    publication_id=publication.id,
                    site_id=site.id,
                    price=item.publication_site_price,
                    image_url=item.image_urls
                    or item.url,  # если есть отдельное изображение
                )
                session.add(pub_site)
            else:
                # Обновляем цену, если запись уже есть
                pub_site.price = item.publication_site_price or pub_site.price
                pub_site.image_url = item.image_urls or item.url or pub_site.image_url

            # 8. Annotation (описание)
            if item.description and item.lang:
                lang = languages_cache.get(item.lang)
                if not lang:
                    lang = session.query(Language).filter_by(lang=item.lang).first()
                    if not lang:
                        lang = Language(lang=item.lang)
                        session.add(lang)
                    languages_cache[item.lang] = lang

                # Проверяем, есть ли уже аннотация на этом языке для этой PublicationSite
                annotation = (
                    session.query(Annotation)
                    .filter_by(publication_site_id=pub_site.id, lang_id=lang.id)
                    .first()
                )

                if not annotation:
                    annotation = Annotation(
                        publication_site_id=pub_site.id,
                        lang_id=lang.id,
                        desctiption=item.description,
                    )
                    session.add(annotation)
                else:
                    annotation.description = item.description

            # 9. Recenzion (ссылка на рецензию)
            if item.recension_link:
                recenzion = (
                    session.query(Recension)
                    .filter_by(publication_id=publication.id, link=item.recension_link)
                    .first()
                )
                if not recenzion:
                    recenzion = Recension(
                        publication_id=publication.id, link=item.recension_link
                    )
                    session.add(recenzion)

        # Один коммит в конце для всей пачки
        session.commit()
