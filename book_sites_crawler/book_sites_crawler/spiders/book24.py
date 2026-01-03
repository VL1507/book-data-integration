from typing import Any, Generator

from scrapy import Spider
from scrapy.http import Response

from book_sites_crawler.items import BookSitesCrawlerItem


class Book24Spider(Spider):
    name = "book24"
    allowed_domains = ["book24.ru"]
    start_urls = ["https://book24.ru/catalog/"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        book_links = response.css("a.product-card__name::attr(href)").getall()
        print(f"{len(book_links)=}")

        # for book_link in book_links:
        #     yield response.follow(book_link, callback=self.parse_book_detail)

        # next_page = response.css("a.pagination__item _link _button _next smartLink::attr(href)").get()
        # if next_page:
        #     yield response.follow(next_page, self.parse)

    def parse_book_detail(
        self, response: Response
    ) -> Generator[BookSitesCrawlerItem, Any, None]:
        item = BookSitesCrawlerItem()

        yield item
