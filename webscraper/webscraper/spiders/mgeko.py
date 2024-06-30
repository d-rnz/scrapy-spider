import scrapy
from webscraper.items import MangaItem


class MgekoSpider(scrapy.Spider):
    name = "mgeko"
    allowed_domains = ["mgeko.cc"]
    start_urls = ["https://www.mgeko.cc/jumbo/manga/"]

    def parse(self, response):
        mangas = response.css('li[class="novel-item"]')

        for manga in mangas:
            manga_item = MangaItem()
            manga_item["cover_art"] = manga.css("img.lazy::attr(data-src)").get()
            manga_item["title"] = manga.css("h4::text").get()
            manga_item["latest_chapter"] = manga.css("h5::text").get()
            manga_item["url"] = manga.css("a.list-body::attr(href)").get()

            yield manga_item

        next_page = response.css(
            "a.mg-pagination-chev:has(i.fa-chevron-right)::attr(href)"
        ).get()

        if next_page and "javascript:void(0)" not in next_page:
            yield response.follow(next_page, self.parse)
