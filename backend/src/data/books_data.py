from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: List[str]
    description: str
    image_url: str

class Publication(BaseModel):
    pass

class BookSitesCrawlerItem(BaseModel):
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


# База данных в виде списка книг
books_db = [
    Book(
        id=1,
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        year=1967,
        genre="Роман",
        description="Философский роман о добре и зле",
        image_filename="book1.jpg",
    ),
    Book(
        id=2,
        title="Преступление и наказание",
        author="Фёдор Достоевский",
        year=1866,
        genre="Психологическая драма",
        description="Роман о моральной дилемме и redemption",
        image_filename="book2.jpg",
    ),
    Book(
        id=3,
        title="Война и мир",
        author="Лев Толстой",
        year=1869,
        genre="Эпопея",
        description="Эпопея о жизни русского общества во время войны с Наполеоном",
        image_filename="book3.jpg",
    ),
    Book(
        id=4,
        title="1984",
        author="Джордж Оруэлл",
        year=1949,
        genre="Антиутопия",
        description="Роман-антиутопия о тоталитарном обществе",
        image_filename="book4.jpg",
    ),
    Book(
        id=5,
        title="Гарри Поттер и философский камень",
        author="Джоан Роулинг",
        year=1997,
        genre="Фэнтези",
        description="Первая книга о приключениях юного волшебника",
        image_filename="book5.jpg",
    ),
]
