import scrapy
from test_task.items import RentalObjectItem

class KelmSpider(scrapy.Spider):
    name = "kelm_spider"
    allowed_domains = ["kelm-immobilien.de"]
    start_urls = ["https://kelm-immobilien.de/immobilien/"]

    def parse(self, response):            
        for url in response.css('h3.property-title a::attr(href)').getall():
            yield response.follow(url, callback=self.scrap_rental_objects)
         
    def scrap_rental_objects(self, response):
        rental_object = RentalObjectItem(
            url = response.request.url,
            title = response.css('h1.property-title::text').get(),
            status = response.css('h2.property-subtitle::text').get(),
            pictures = response.css('div#immomakler-galleria a::attr(href)').getall(),
            rent_price = float(
                response.css('li.data-kaufpreis .col-sm-7::text').get().split()[0]
            )*1000,
            description = '\n'.join(
                response.css('div.panel-body h3::text,div.panel-body p::text').getall()    
            ),
            phone_number = response.css('div.tel a::text').get(),
            email = response.css('div.email a::text').get()
        )

        yield rental_object