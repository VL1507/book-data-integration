from typing import Any, Generator

from scrapy import Request, Spider
from scrapy.http import Response

from book_sites_crawler.items import BookSitesCrawlerItem


class ChitaiGorodSpider(Spider):
    name = "chitai-gorod"
    allowed_domains = ["chitai-gorod.ru"]
    start_urls = ["https://chitai-gorod.ru/catalog/books-18030"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        book_links = response.css("a.product-card__title::attr(href)").getall()
        print(f"{len(book_links)=}")

        # for book_link in book_links:
        #     yield response.follow(book_link, callback=self.parse_book_detail)

        # next_page = response.css("div.app-catalog__pagination a::attr(href)").get()
        # if next_page:
        #     yield response.follow(next_page, self.parse)

    def parse_book_detail(
        self, response: Response
    ) -> Generator[BookSitesCrawlerItem, Any, None]:
        item = BookSitesCrawlerItem()

        yield item
