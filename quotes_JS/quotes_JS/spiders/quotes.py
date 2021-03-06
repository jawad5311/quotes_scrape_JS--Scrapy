import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    # Splash script that needs to be executed
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
        """ Make request using SplashRequest class in splash module """
        yield SplashRequest(
            url='https://quotes.toscrape.com/js',
            callback=self.parse,
            endpoint='execute',  # Sets the endpoint to execute the script first
            args={
                'lua_source': self.script  # Script needed to be executed
            }
        )

    def parse(self, response):
        """ Responsible for scrapping required data """
        quotes = response.xpath("//div[@class='quote']")  # Get holds of the divs containing quotes

        for quote in quotes:
            yield {
                'quote': quote.xpath(".//span[@class='text']/text()").get(),
                'author': quote.xpath(".//span[2]/small[@class='author']/text()").get(),
                'tags': quote.xpath(".//div[@class='tags']/a/text()").getall()
            }

        # Grabs the URL from the next button on the page
        next_page = response.xpath("//li[@class='next']/a/@href").get()

        if next_page:
            """ Execute the following code if the next button is available """
            absolute_url = f"https://quotes.toscrape.com{next_page}"  # Creates absolute URL for the next page
            # Using SplashRequest class calls the parse method again
            yield SplashRequest(
                url=absolute_url,
                callback=self.parse,
                endpoint='execute',
                args={
                    'lua_source': self.script  # Script needed to be executed
                }
            )

