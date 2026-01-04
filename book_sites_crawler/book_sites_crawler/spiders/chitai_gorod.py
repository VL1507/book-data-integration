from typing import Any, Generator

from scrapy import Request, Spider
from scrapy.http import Response

from book_sites_crawler.items import BookSitesCrawlerItem


class ChitaiGorodSpider(Spider):
    name = "chitai-gorod"
    allowed_domains = ["chitai-gorod.ru"]
    start_urls = ["https://chitai-gorod.ru/catalog/books-18030"]

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
        # "LOG_LEVEL": "INFO",
    }
    page_count_limit = 40
    page_count = 0

    def parse(self, response: Response, **kwargs: Any) -> Any:
        book_links = response.css("a.product-card__title::attr(href)").getall()

        self.logger.info(
            f"\n\n{len(book_links)=}\n{self.page_count}/{self.page_count_limit}\n"
        )

        for book_link in book_links:
            yield response.follow(book_link, callback=self.parse_book_detail)

        # next_page = response.css("div.app-catalog__pagination a::attr(href)").get()
        # if next_page:
        #     if self.page_count >= self.page_count_limit:
        #         return
        #     self.page_count += 1
        #     yield response.follow(next_page, self.parse)

    def parse_book_detail(
        self, response: Response
    ) -> Generator[BookSitesCrawlerItem, Any, None]:
        self.logger.info(response.url)

        item = BookSitesCrawlerItem()

        yield item
