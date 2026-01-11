from typing import Optional

from sqlalchemy import REAL, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class AdditionalCharacteristics(Base):
    __tablename__ = "AdditionalCharacteristics"

    name: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Authors(Base):
    __tablename__ = "Authors"

    name: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class CoveragesTypes(Base):
    __tablename__ = "CoveragesTypes"

    name: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Genre(Base):
    __tablename__ = "Genre"

    genre: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class IllustrationTypes(Base):
    __tablename__ = "IllustrationTypes"

    name: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Language(Base):
    __tablename__ = "Language"

    lang: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class PublishingHouses(Base):
    __tablename__ = "PublishingHouses"

    name: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[Optional[str]] = mapped_column(String)


class Sites(Base):
    __tablename__ = "Sites"

    site: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Publication(Base):
    __tablename__ = "Publication"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    

class ISBN(Base):
    __tablename__ = "ISBN"

    isbn: Mapped[str] = mapped_column(String, primary_key=True)
    publication_site_id: Mapped[int] = mapped_column(ForeignKey("PublicationSite.id"))
    publisher_id: Mapped[int] = mapped_column(ForeignKey("PublishingHouses.id"))

class Characteristics(Base):
    __tablename__ = "Characteristics"
    publication_site_id: Mapped[int] = mapped_column(ForeignKey("PublicationSite.id"), primary_key=True)

    year: Mapped[int] = mapped_column(Integer)
    page_count: Mapped[int] = mapped_column(Integer)
    dim_x: Mapped[Optional[int]] = mapped_column(Integer)
    dim_y: Mapped[Optional[int]] = mapped_column(Integer)
    dim_z: Mapped[Optional[int]] = mapped_column(Integer)
    cover_id: Mapped[int] = mapped_column(ForeignKey("CoveragesTypes.id"))
    illustration_id: Mapped[int] = mapped_column(
        ForeignKey("IllustrationTypes.id")
    )


class PublicationAuthors(Base):
    __tablename__ = "PublicationAuthors"
    publication_id: Mapped[int] = mapped_column(
        ForeignKey("Publication.id"), primary_key=True, nullable=False
    )
    authors_id: Mapped[int] = mapped_column(
        ForeignKey("Authors.id"), primary_key=True, nullable=False
    )


class PublicationSite(Base):
    __tablename__ = "PublicationSite"

    publication_id: Mapped[int] = mapped_column(ForeignKey("Publication.id"))
    site_id: Mapped[int] = mapped_column(ForeignKey("Sites.id"))
    price: Mapped[float] = mapped_column(REAL)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[Optional[str]] = mapped_column(String)


class Recension(Base):
    __tablename__ = "Recension"

    publication_id: Mapped[int] = mapped_column(ForeignKey("Publication.id"))
    link: Mapped[str] = mapped_column(String)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Annotation(Base):
    __tablename__ = "Annotation"

    publication_site_id: Mapped[int] = mapped_column(
        ForeignKey("PublicationSite.id"), primary_key=True
    )
    lang_id: Mapped[int] = mapped_column(ForeignKey("Language.id"), primary_key=True)
    description: Mapped[str] = mapped_column(Text)


class CharacteristicsAdditional(Base):
    __tablename__ = "CharacteristicsAdditional"

    characteristic_id: Mapped[int] = mapped_column(
        ForeignKey("Characteristics.publication_id"), primary_key=True
    )
    additional_id: Mapped[int] = mapped_column(
        ForeignKey("AdditionalCharacteristics.id"), primary_key=True
    )
    value: Mapped[str] = mapped_column(Text)


class CharacteristicsGenre(Base):
    __tablename__ = "CharacteristicsGenre"
    characteristic_id: Mapped[int] = mapped_column(
        ForeignKey("Characteristics.publication_site_id"), primary_key=True, nullable=False
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("Genre.id"), primary_key=True, nullable=False
    )
