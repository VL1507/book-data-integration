from pydantic import BaseModel


class BookForListSchema(BaseModel):
    publication_id: int
    title: str
    authors: list[str]
    years: list[int]
    genres: list[str]
    image_url: str


class PublicationSiteInfo(BaseModel):
    year: int
    page_count: int
    price: float
    image_url: str
    site_name: str
    site_url: str
    illustration_type: str | None
    coverages_type: str | None
    dim_x: int | None
    dim_y: int | None
    dim_z: int | None


class BookFull(BaseModel):
    publication_id: int
    title: str
    authors: list[str]
    genres: list[str]
    annotation: str | None
    publication_site_info: list[PublicationSiteInfo]
