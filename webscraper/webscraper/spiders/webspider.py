import scrapy


class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    allowed_domains = ["asuracomic.net"]
    start_urls = ["https://asuracomic.net"]

    def parse(self, response):
        mangas = response.css("div.utao.styletwo")

        for manga in mangas:
            yield {
                "image": manga.css("img::attr(src)").get(),
                "title": manga.css("h4::text").get(),
                "chapter": manga.css("ul.Manhwa li a::text").get(),
                "link": manga.css("a.series::attr(href)").get(),
            }

        next_page = response.css("a.r::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
