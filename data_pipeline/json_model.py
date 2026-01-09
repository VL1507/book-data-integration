from dataclasses import dataclass


@dataclass
class BookSitesCrawlerItem:
    isbn: list[str]
    year: int | None
    page_count: int | None
    dim_x: int | None
    dim_y: int | None
    dim_z: int | None

    books_name: str | None

    authors_name: list[str]

    sites_site: str
    sites_url: str

    publication_site_price: float | None

    lang: str | None

    description: str | None

    publishing_houses_name: str | None
    publishing_houses_url: str | None

    recension_link: str | None

    illustration_types_name: str | None

    coverages_types_name: str | None

    image_urls: str | None

    url: str | None

    genre: str | None
