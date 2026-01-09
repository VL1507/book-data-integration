from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Column, ForeignKey, Integer, REAL, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class AdditionalCharacteristics(Base):
    __tablename__ = 'AdditionalCharacteristics'

    name: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    CharacteristicsAdditional: Mapped[List['CharacteristicsAdditional']] = relationship('CharacteristicsAdditional', back_populates='additional')


class Authors(Base):
    __tablename__ = 'Authors'

    name: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    publication: Mapped[List['Pubication']] = relationship('Pubication', secondary='PublicationAuthors', back_populates='authors')


class Books(Base):
    __tablename__ = 'Books'

    name: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    Pubication: Mapped[List['Pubication']] = relationship('Pubication', back_populates='book')


class CoveragesTypes(Base):
    __tablename__ = 'CoveragesTypes'

    name: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    characteristics: Mapped[List['Characteristics']] = relationship('Characteristics', back_populates='cover')


class Genre(Base):
    __tablename__ = 'Genre'

    genre: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    characteristic: Mapped[List['Characteristics']] = relationship('Characteristics', secondary='CharacteristicsGenre', back_populates='genre')


class IllustatinonTypes(Base):
    __tablename__ = 'IllustatinonTypes'

    name: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    characteristics: Mapped[List['Characteristics']] = relationship('Characteristics', back_populates='illustration')


class Language(Base):
    __tablename__ = 'Language'

    lang: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    annotation: Mapped[List['Annotation']] = relationship('Annotation', back_populates='lang')


class PublishingHouses(Base):
    __tablename__ = 'PublishingHouses'

    name: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    url: Mapped[Optional[str]] = mapped_column(String)

    pubication: Mapped[List['Pubication']] = relationship('Pubication', back_populates='publisher')


class Sites(Base):
    __tablename__ = 'Sites'

    site: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    publicationSite: Mapped[List['PublicationSite']] = relationship('PublicationSite', back_populates='site')


class Pubication(Base):
    __tablename__ = 'Pubication'

    book_id: Mapped[int] = mapped_column(ForeignKey('Books.id'))
    publisher_id: Mapped[int] = mapped_column(ForeignKey('PublishingHouses.id'))
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    authors: Mapped[List['Authors']] = relationship('Authors', secondary='PublicationAuthors', back_populates='publication')
    book: Mapped['Books'] = relationship('Books', back_populates='pubication')
    publisher: Mapped['PublishingHouses'] = relationship('PublishingHouses', back_populates='pubication')
    publicationSite: Mapped[List['PublicationSite']] = relationship('PublicationSite', back_populates='publication')
    recenzion: Mapped[List['Recenzion']] = relationship('Recenzion', back_populates='publication')


class Characteristics(Pubication):
    __tablename__ = 'Characteristics'

    ISBN: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    page_count: Mapped[int] = mapped_column(Integer)
    publication_id: Mapped[Optional[int]] = mapped_column(ForeignKey('Pubication.id'), primary_key=True)
    dim_x: Mapped[Optional[int]] = mapped_column(Integer)
    dim_y: Mapped[Optional[int]] = mapped_column(Integer)
    dim_z: Mapped[Optional[int]] = mapped_column(Integer)
    cover_id: Mapped[Optional[int]] = mapped_column(ForeignKey('CoveragesTypes.id'))
    illustration_id: Mapped[Optional[int]] = mapped_column(ForeignKey('IllustatinonTypes.id'))

    cover: Mapped[Optional['CoveragesTypes']] = relationship('CoveragesTypes', back_populates='Characteristics')
    illustration: Mapped[Optional['IllustatinonTypes']] = relationship('IllustatinonTypes', back_populates='Characteristics')
    genre: Mapped[List['Genre']] = relationship('Genre', secondary='CharacteristicsGenre', back_populates='characteristic')
    CharacteristicsAdditional: Mapped[List['CharacteristicsAdditional']] = relationship('CharacteristicsAdditional', back_populates='characteristic')


class PublicationAuthors(Base):
    __tablename__ = 'PublicationAuthors'
    publication_id: Mapped[int] = mapped_column(ForeignKey('Pubication.id'), primary_key=True, nullable=False)
    authors_id: Mapped[int] = mapped_column(ForeignKey('Authors.id'), primary_key=True, nullable=False)



class PublicationSite(Base):
    __tablename__ = 'PublicationSite'

    publication_id: Mapped[int] = mapped_column(ForeignKey('Pubication.id'))
    site_id: Mapped[int] = mapped_column(ForeignKey('Sites.id'))
    price: Mapped[float] = mapped_column(REAL)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    image_url: Mapped[Optional[str]] = mapped_column(String)

    publication: Mapped['Pubication'] = relationship('Pubication', back_populates='PublicationSite')
    site: Mapped['Sites'] = relationship('Sites', back_populates='PublicationSite')
    Annotation: Mapped[List['Annotation']] = relationship('Annotation', back_populates='publication_site')


class Recenzion(Base):
    __tablename__ = 'Recenzion'

    publication_id: Mapped[int] = mapped_column(ForeignKey('Pubication.id'))
    link: Mapped[str] = mapped_column(String)
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    publication: Mapped['Pubication'] = relationship('Pubication', back_populates='Recenzion')


class Annotation(Base):
    __tablename__ = 'Annotation'

    publication_site_id: Mapped[int] = mapped_column(ForeignKey('PublicationSite.id'), primary_key=True)
    lang_id: Mapped[int] = mapped_column(ForeignKey('Language.id'), primary_key=True)
    desctiption: Mapped[str] = mapped_column(Text)

    lang: Mapped['Language'] = relationship('Language', back_populates='Annotation')
    publication_site: Mapped['PublicationSite'] = relationship('PublicationSite', back_populates='Annotation')


class CharacteristicsAdditional(Base):
    __tablename__ = 'CharacteristicsAdditional'

    characteristic_id: Mapped[int] = mapped_column(ForeignKey('Characteristics.publication_id'), primary_key=True)
    additional_id: Mapped[int] = mapped_column(ForeignKey('AdditionalCharacteristics.id'), primary_key=True)
    value: Mapped[str] = mapped_column(Text)

    additional: Mapped['AdditionalCharacteristics'] = relationship('AdditionalCharacteristics', back_populates='CharacteristicsAdditional')
    characteristic: Mapped['Characteristics'] = relationship('Characteristics', back_populates='CharacteristicsAdditional')


class CharacteristicsGenre(Base):
    __tablename__ = 'CharacteristicsGenre'
    characteristic_id: Mapped[int] = mapped_column(ForeignKey('Characteristics.publication_id'), primary_key=True, nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey('Genre.id'), primary_key=True, nullable=False)
