import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com/js']
    start_urls = ['http://quotes.toscrape.com/js/']

    def parse(self, response):
        pass
