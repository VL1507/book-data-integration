from typing import Any, Generator

from scrapy import Spider
from scrapy.http import Response

from book_sites_crawler.items import BookSitesCrawlerItem


class LabirintSpider(Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    start_urls = [
        # "https://labirint.ru/books/",
        "https://www.labirint.ru/genres/1852/",
    ]

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
    page_count_limit = 40
    page_count = 0

    def parse(self, response: Response, **kwargs: Any) -> Any:
        book_links = response.css("a.cover.genres-cover::attr(href)").getall()

        self.logger.info(
            f"\n\n{len(book_links)=}\n{self.page_count}/{self.page_count_limit}\n"
        )

        for book_link in book_links:
            if book_link and "/books/" in book_link:
                yield response.follow(book_link, callback=self.parse_book_detail)

        next_page = response.css("a.pagination-next__text::attr(href)").get()
        if next_page:
            if self.page_count >= self.page_count_limit:
                return
            self.page_count += 1
            yield response.follow(next_page, self.parse)

    def parse_book_detail(
        self, response: Response
    ) -> Generator[BookSitesCrawlerItem, Any, None]:
        self.logger.info(response.url)

        characteristics = response.css("div#сharacteristics")

        item = BookSitesCrawlerItem()

        item["isbn"] = list(
            map(
                lambda isbn: isbn.replace("-", ""),
                (
                    characteristics.css(
                        'div._feature_mmfyx_1 div._name_mmfyx_9:contains("ISBN") ~ div.text-black span::text'
                    )
                    .get(default="")
                    .split(", ")
                ),
            )
        )

        if len(item["isbn"]) == 0 or (len(item["isbn"]) == 1 and item["isbn"][0] == ""):
            return

        year = characteristics.css(
            'div._name_mmfyx_9:contains("Издательство") + div span:last-child::text'
        ).get()
        if year is not None and year.isdigit():
            year = int(year)
        item["year"] = year

        page_count = characteristics.css(
            'div._feature_mmfyx_1 div._name_mmfyx_9:contains("Страниц") ~ div.text-black span::text'
        ).get()
        if page_count is not None and page_count.isdigit():
            page_count = int(page_count)
        item["page_count"] = page_count

        dim = characteristics.css(
            'div._feature_mmfyx_1 div._name_mmfyx_9:contains("Размеры") ~ div.text-black span::text'
        ).get()
        if dim is None:
            item["dim_x"] = None
            item["dim_y"] = None
            item["dim_z"] = None
        else:
            dim_split = dim.split("x")
            dim_split.extend([None, None, None])  # type: ignore
            item["dim_x"], item["dim_y"], item["dim_z"], *_ = dim_split

        item["books_name"] = response.xpath("//h1/text()[1]").get()

        item["authors_name"] = characteristics.css(
            'div._name_mmfyx_9:contains("Автор") + div a::text'
        ).getall()

        item["genre"] = response.css(
            'div#сharacteristics div._name_mmfyx_9:contains("Жанр") + div a::text'
        ).getall()

        item["sites_site"] = "labirint"
        item["sites_url"] = self.allowed_domains[0]

        # PublicationSite
        current_price = response.xpath(
            '//*[@id="__nuxt"]/main/article/div[2]/meta[@itemprop="price"]/@content'
        ).get()
        if current_price:
            current_price = current_price.replace("\xa0", "").strip()
        item["publication_site_price"] = current_price

        # Language
        item["lang"] = characteristics.css(
            'div._feature_mmfyx_1 div._name_mmfyx_9:contains("Язык") ~ div.text-black span::text'
        ).get()

        # Annotation
        full_text = response.xpath(
            '//*[@id="annotation"]/div[2]/div/div[1]/div[1]//text()'
        ).getall()
        item["description"] = " ".join([t.strip() for t in full_text if t.strip()])

        item["publishing_houses_name"] = characteristics.css(
            'div._name_mmfyx_9:contains("Издательство") + div a::text'
        ).get()
        # TODO: сейчас ссылка на лабиринт а не на само издательство
        item["publishing_houses_url"] = characteristics.css(
            'div._name_mmfyx_9:contains("Издательство") + div a::attr(href)'
        ).get()

        # Recension
        # item["recension_link"] = ...

        # IllustrationTypes
        item["illustration_types_name"] = characteristics.css(
            'div._name_mmfyx_9:contains("Иллюстрации") ~ div.text-black span::text'
        ).get()

        # CoveragesTypes
        item["coverages_types_name"] = characteristics.css(
            'div._name_mmfyx_9:contains("Тип обложки") ~ div.text-black span::text'
        ).get()

        # AdditionalCharacteristics # TODO: что это и зачем
        # item["additional_characteristics_name"] = ...
        # CharacteristicsToAdditional
        # item["characteristics_to_additional_value"] = ...
        # item["additional_characteristics"] = ...

        labirint_book_id = response.url.split("/")[-2]
        item["image_urls"] = (
            f"https://static10.labirint.ru/books/{labirint_book_id}/cover.jpg"
        )

        item["url"] = response.url

        yield item
