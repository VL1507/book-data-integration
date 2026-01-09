from dataclasses import dataclass

from dataclasses import field


@dataclass
class BookSitesCrawlerItem:
    isbn: list[str] = field(default_factory=list)
    year: int | None = field(default=None)
    page_count: int | None = field(default=None)
    dim_x: int | None = field(default=None)
    dim_y: int | None = field(default=None)
    dim_z: int | None = field(default=None)

    books_name: str | None = field(default=None)

    authors_name: list[str] = field(default_factory=list)

    sites_site: str = field(default="")
    sites_url: str = field(default="")

    publication_site_price: float | None = field(default=None)

    lang: str | None = field(default=None)

    description: str | None = field(default=None)

    publishing_houses_name: str | None = field(default=None)
    publishing_houses_url: str | None = field(default=None)

    recension_link: str | None = field(default=None)

    illustration_types_name: str | None = field(default=None)

    coverages_types_name: str | None = field(default=None)

    image_urls: str | None = field(default=None)

    url: str | None = field(default=None)

    genre: list[str] = field(default_factory=list)
