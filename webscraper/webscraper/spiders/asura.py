import scrapy
from webscraper.items import MangaItem


class AsuraSpider(scrapy.Spider):
    name = "asura"
    allowed_domains = ["asuracomic.net"]
    start_urls = ["https://asuracomic.net"]

    def parse(self, response):
        mangas = response.css("div.utao.styletwo")

        for manga in mangas:
            manga_item = MangaItem()
            manga_item["cover_art"] = manga.css("img::attr(src)").get()
            manga_item["title"] = manga.css("h4::text").get()
            manga_item["latest_chapter"] = manga.css("ul.Manhwa li a::text").get()
            manga_item["url"] = manga.css("a.series::attr(href)").get()

            yield manga_item

        next_page = response.css("a.r::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
