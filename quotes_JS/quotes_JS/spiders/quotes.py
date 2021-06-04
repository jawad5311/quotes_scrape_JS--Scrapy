import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com/js']
    start_urls = ['http://quotes.toscrape.com/js/']

    script = """
    function main(splash, args)
  
        splash.private_mode_enabled = false
        
        assert(splash:go(args.url))
        assert(splash:wait(1))
        splash:set_viewport_full()
        
        return splash:html()
  
    end
    """

    def start_requests(self):
        yield SplashRequest(
            url='https://quotes.toscrape.com/js',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        print(response.body)
