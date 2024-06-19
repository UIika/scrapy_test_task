import scrapy
from test_task.items import RentalObjectItem

class AdentzSpider(scrapy.Spider):
    name = "adentz_spider"
    allowed_domains = ["www.adentz.de"]
    start_urls = ["https://www.adentz.de/wohnung-mieten-rostock/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'test_task.selenium_middleware.SeleniumMiddleware': 491,
        }
    }
    
    def parse(self, response):
        proper_urls = [
            response.request.url+'#/expose'+url.split('\"')[1] for url in
            response.css('div.hm_listbox a::attr(href)').getall()
        ]
        for url in proper_urls:
            yield response.follow(url, callback=self.scrap_rental_objects, dont_filter=True)
         
    def scrap_rental_objects(self, response):
        rental_object = RentalObjectItem(
            url = response.request.url,
            title = response.css('div.iwWidget h1::text').get(),
            status = response.css('div.iwWidget span::text').getall()[1],
            pictures = [
                img.replace('100x70', '640x0') for img in
                response.css('a.thumbclick img::attr(src)').getall()  
            ],
            rent_price = float(
                response.css(
                    'div.iwWidget span::text'
                ).getall()[0].split()[1].replace('.', '').replace(',','.')
            ),
            description = '\n'.join(
                response.css(
                    'div.hm_expose_full_width p::text, '\
                    'div.hm_expose_full_width strong::text'    
                ).getall()    
            ),
            phone_number = response.css('div.hm_box_02 span::text').getall()[1],
            email = response.css('div.avia_textblock a::text').get()
        )

        yield rental_object