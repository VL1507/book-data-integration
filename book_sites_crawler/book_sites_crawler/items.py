from scrapy import Field, Item


class BookSitesCrawlerItem(Item):
    # Characteristics
    isbn = Field()
    year = Field()
    page_count = Field()
    dim_x = Field()
    dim_y = Field()
    dim_z = Field()

    # Books
    books_name = Field()

    # Authors
    authors_name = Field()

    # Sites
    sites_site = Field()
    sites_url = Field()

    # PublicationSite
    publication_site_price = Field()

    # Language
    lang = Field()

    # Annotation
    description = Field()

    # PublishingHouses
    publishing_houses_name = Field()
    publishing_houses_url = Field()

    # Recension
    recension_link = Field()

    # IllustrationTypes
    illustration_types_name = Field()

    # CoveragesTypes
    coverages_types_name = Field()

    # AdditionalCharacteristics # TODO: что это и зачем
    # additional_characteristics_name = Field()
    # CharacteristicsToAdditional
    # characteristics_to_additional_value = Field()
    additional_characteristics = Field()

    image_urls = Field()
    images = Field()

    url = Field()

    genre = Field()
