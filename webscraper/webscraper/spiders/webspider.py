import scrapy


class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    allowed_domains = ["asuracomic.net"]
    start_urls = ["https://asuracomic.net"]

    def parse(self, response):
        pass
