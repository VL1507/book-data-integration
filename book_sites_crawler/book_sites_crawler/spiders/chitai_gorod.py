from typing import Any, Generator

from scrapy import Spider
from scrapy.http import Response

from book_sites_crawler.items import BookSitesCrawlerItem


class ChitaiGorodSpider(Spider):
    name = "chitai-gorod"
    allowed_domains = ["chitai-gorod.ru"]
    start_urls = ["https://www.chitai-gorod.ru/catalog/books-18030"]

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
        "CONCURRENT_REQUESTS": 16,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 8,
        #
        "DOWNLOAD_DELAY": 0.5,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "DOWNLOAD_TIMEOUT": 30,
        #
        "HTTPCACHE_ENABLED": True,
        #
        "LOG_LEVEL": "INFO",
    }
    page_count_limit = 20
    page_count = 0

    def parse(self, response: Response, **kwargs: Any) -> Any:
        book_links = response.css("a.product-card__title::attr(href)").getall()

        self.logger.info(
            f"\n\n{len(book_links)=}\n{self.page_count}/{self.page_count_limit}\n"
        )

        for book_link in book_links:
            yield response.follow(book_link, callback=self.parse_book_detail)

        next_page = response.css("div.app-catalog__pagination a::attr(href)").get()
        if next_page:
            if self.page_count >= self.page_count_limit:
                return
            self.page_count += 1
            yield response.follow(next_page, self.parse)

    def parse_book_detail(
        self, response: Response
    ) -> Generator[BookSitesCrawlerItem, Any, None]:
        self.logger.info(response.url)

        item = BookSitesCrawlerItem()

        characteristics = response.css("div#description")

        item["isbn"] = list(
            map(
                lambda isbn: isbn.replace("-", "").strip(),
                characteristics.css('span[itemprop="isbn"] span::text').getall(),
            )
        )

        if len(item["isbn"]) == 0 or (len(item["isbn"]) == 1 and item["isbn"][0] == ""):
            return

        item["year"] = characteristics.css(
            'span[itemprop="datePublished"] span::text'
        ).get()

        item["page_count"] = characteristics.css(
            'span[itemprop="numberOfPages"] span::text'
        ).get()

        dim = characteristics.css('span[itemprop="size"] span::text').get()
        if dim is None:
            item["dim_x"] = None
            item["dim_y"] = None
            item["dim_z"] = None
        else:
            dim_split = dim.strip().split()[0].split("x")
            dim_split.extend([None, None, None])  # type: ignore
            item["dim_x"], item["dim_y"], item["dim_z"], *_ = dim_split

        item["books_name"] = response.css("h1.product-detail-page__title::text").get()

        item["authors_name"] = list(
            map(
                lambda author_name: author_name.replace(",", "").strip(),
                response.css("ul.product-authors a::text").getall(),
            )
        )

        item["genre"] = characteristics.css(
            'span[itemprop="comicGenres"] a::text'
        ).getall()

        item["sites_site"] = "chitai-gorod"
        item["sites_url"] = self.allowed_domains[0]

        # PublicationSite
        current_price = response.css("span.product-offer-price__actual::text").get()
        if current_price:
            current_price = current_price.replace("\xa0", "").replace("₽", "").strip()
        item["publication_site_price"] = current_price

        # Language # TODO: на сайте не указывается язык
        item["lang"] = "Русский"

        # Annotation
        full_text = characteristics.css(
            "article.product-detail-page__detail-text::text"
        ).getall()
        item["description"] = " ".join([t.strip() for t in full_text if t.strip()])

        item["publishing_houses_name"] = characteristics.css(
            'span[itemprop="publisher"] a::text'
        ).get()

        publishing_houses_url = characteristics.css(
            'span[itemprop="publisher"] a::attr(href)'
        ).get()
        if publishing_houses_url:
            item["publishing_houses_url"] = response.urljoin(publishing_houses_url)
        else:
            item["publishing_houses_url"] = None

        # Recension
        # item["recension_link"] = ...

        # IllustrationTypes # TODO: нет такой характеристики на сайте
        item["illustration_types_name"] = None

        # CoveragesTypes
        coverages_types_name = characteristics.css(
            'span[itemprop="bookFormat"] span::text'
        ).get()
        if coverages_types_name:
            item["coverages_types_name"] = coverages_types_name.strip()
        else:
            item["coverages_types_name"] = None

        # AdditionalCharacteristics # TODO: что это и зачем
        # item["additional_characteristics_name"] = ...
        # CharacteristicsToAdditional
        # item["characteristics_to_additional_value"] = ...
        # item["additional_characteristics"] = ...

        item["image_urls"] = response.css(
            'meta[property="og:image"]::attr(content)'
        ).get()

        item["url"] = response.url

        yield item
