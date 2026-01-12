from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: list[str]
    year: int
    genre: list[str]
    image_url: str


class Annotation(BaseModel):
    language: str
    annotation: str


class Publication(BaseModel):
    id: int
    isbn: str
    sites: list[str]
    authors_name: list[str]
    annotations: list[Annotation]
    page_count: int
    dim_x: int | None
    dim_y: int | None
    dim_z: int | None
    illustration_types_name: str | None
    coverages_types_name: str | None
    image_url: str | None


class BookInfo(BaseModel):
    id: int
    publications: list[Publication]
    title: str
    authors: list[str]
    year: int
