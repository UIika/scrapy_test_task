import scrapy
from test_task.items import RentalObjectItem

class BostadSpider(scrapy.Spider):
    name = "bostad_spider"
    allowed_domains = ["bostad.herbo.se"]
    start_urls = ["https://bostad.herbo.se/HSS/Object/object_list.aspx?cmguid=4e6e781e-5257-403e-b09d-7efc8edb0ac8&objectgroup=1&action=Available"]

    def parse(self, response):
        for url in response.css(
            'td.gridcell a:not([class^="icon_objectlist_map"])::attr(href)'
        ).getall():
            yield response.follow(url, callback=self.scrap_rental_objects)
            
         
    def scrap_rental_objects(self, response):
        rental_object = RentalObjectItem(
            url = response.request.url,
            title = response.css('h1.pagetitle::text').get(),
            status = response.css('li.right span::text').get(),
            pictures = [
                'https://'+self.allowed_domains[0]+image for image in
                response.css('div.image-slideshow img::attr(src)').getall()
            ],
            rent_price = float(response.css(
                'ul#ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_trCost li.right::text'    
            ).get()[:-2].replace(' ','')),
            description = '\n'.join(
                response.css(
                    'div#ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_divOverview p::text'
                ).getall()
            ),
            phone_number = response.css(
                'ul#ctl00_ctl01_DefaultSiteContentPlaceHolder1_Col1_ulObjectID li.right::text'    
            ).get(),
            email = None
        )

        yield rental_object