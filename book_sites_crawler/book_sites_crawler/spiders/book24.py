from typing import Any, Generator

from scrapy import Spider
from scrapy.http import Response

from book_sites_crawler.items import BookSitesCrawlerItem


class Book24Spider(Spider):
    name = "book24"
    allowed_domains = ["book24.ru"]
    start_urls = ["https://book24.ru/catalog/"]

    custom_settings = {
        # "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
        "CONCURRENT_REQUESTS": 16,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8,
        # "DOWNLOAD_DELAY": 0.5,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
        # "DOWNLOAD_TIMEOUT": 30,
        "HTTPCACHE_ENABLED": True,
        # "ITEM_PIPELINES": {
        #     # 'book_parsers.pipelines.BookImagesPipeline=100,
        #     "scrapy.pipelines.images.ImagesPipeline": 1
        # },
        # "IMAGES_STORE": "data/images/labirint/1",
        # "IMAGES_URLS_FIELD": "image_urls",
        # "IMAGES_RESULT_FIELD": "images",
    }

    def parse(self, response: Response, **kwargs: Any) -> Any:
        book_links = response.css("a.product-card__name::attr(href)").getall()
        print(f"{len(book_links)=}")

        for book_link in book_links:
            yield response.follow(book_link, callback=self.parse_book_detail)

        # next_page = response.css("a.pagination__item _link _button _next smartLink::attr(href)").get()
        # if next_page:
        #     yield response.follow(next_page, self.parse)

    def parse_book_detail(
        self, response: Response
    ) -> Generator[BookSitesCrawlerItem, Any, None]:
        item = BookSitesCrawlerItem()

        characteristics = response.css("#product-characteristic > dl")

        item["isbn"] = list(
            map(
                lambda isbn: isbn.replace("-", ""),
                (
                    characteristics.css("button.isbn-product::text")
                    .get(default="")
                    .strip()
                    .split(", ")
                ),
            )
        )

        item["year"] = (
            characteristics.xpath(
                './/span[contains(., "Год издания")]/ancestor::dt/following-sibling::dd[@class="product-characteristic__value"]/text()'
            )
            .get(default="")
            .strip()
        )

        item["page_count"] = (
            characteristics.xpath(
                './/span[contains(., " Количество страниц: ")]/ancestor::dt/following-sibling::dd[@class="product-characteristic__value"]/text()'
            )
            .get(default="")
            .strip()
        )

        dim = characteristics.xpath(
            './/span[contains(., " Формат: ")]/ancestor::dt/following-sibling::dd[@class="product-characteristic__value"]/text()'
        ).get()
        if dim is None:
            item["dim_x"] = None
            item["dim_y"] = None
            item["dim_z"] = None
        else:
            dim_split = dim.strip().split()[0].split("x")
            dim_split.extend([None, None, None])  # type: ignore
            item["dim_x"], item["dim_y"], item["dim_z"], *_ = dim_split

        books_name = response.css(
            "div.breadcrumbs.product-detail-page__breadcrumbs > ol > li.breadcrumbs__item._last-item > span::text"
        ).get()
        if books_name:
            item["books_name"] = books_name.strip()
        else:
            item["books_name"] = None

        item["authors_name"] = characteristics.xpath(
            './/span[contains(., " Автор: ")]/ancestor::dt/following-sibling::dd[@class="product-characteristic__value"]/a/text()'
        ).getall()

        item["genre"] = characteristics.xpath(
            './/span[contains(., " Раздел: ")]/ancestor::dt/following-sibling::dd[@class="product-characteristic__value"]/a/text()'
        ).getall()

        item["sites_site"] = "book24"
        item["sites_url"] = self.allowed_domains[0]

        # PublicationSite
        current_price = response.css(
            "span.app-price.product-sidebar-price__price::text"
        ).get()
        if current_price:
            current_price = current_price.replace("\xa0", "").replace("₽", "").strip()
        item["publication_site_price"] = current_price

        # # Language # TODO: на сайте не указывается язык
        item["lang"] = "Русский"

        # # Annotation
        # full_text = response.xpath(
        #     '//*[@id="annotation"]/div[2]/div/div[1]/div[1]//text()'
        # ).getall()
        # item["description"] = " ".join([t.strip() for t in full_text if t.strip()])

        # item["publishing_houses_name"] = characteristics.css(
        #     'div._name_mmfyx_9:contains("Издательство") + div a::text'
        # ).get()
        # # TODO: сейчас ссылка на лабиринт а не на само издательство
        # item["publishing_houses_url"] = characteristics.css(
        #     'div._name_mmfyx_9:contains("Издательство") + div a::attr(href)'
        # ).get()

        # # Recension
        # # item["recension_link"] = ...

        # # IllustrationTypes
        # item["illustration_types_name"] = characteristics.css(
        #     'div._name_mmfyx_9:contains("Иллюстрации") ~ div.text-black span::text'
        # ).get()

        # # CoveragesTypes
        # item["coverages_types_name"] = characteristics.css(
        #     'div._name_mmfyx_9:contains("Тип обложки") ~ div.text-black span::text'
        # ).get()

        # # AdditionalCharacteristics # TODO: что это и зачем
        # # item["additional_characteristics_name"] = ...
        # # CharacteristicsToAdditional
        # # item["characteristics_to_additional_value"] = ...
        # # item["additional_characteristics"] = ...

        image_url = response.xpath(
            '//div[@class="product-poster__main-slide"][1]//source/@srcset'
        ).get()
        if image_url:
            item["image_urls"] = "https:" + image_url.split()[0].strip()
        else:
            item["image_urls"] = None

        item["url"] = response.url

        yield item
