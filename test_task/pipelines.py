import json
import os


countries: dict[str,str] = {
    'de': 'Germany',
    'se': 'Sweden'
}    

OUTPUT_FILE_NAME = 'output.json'

class RentalScrapperPipeline:
    def get_country_from_domain(self, domain: str) -> str:
        top_level_domain = domain.split('.')[-1]
        return countries[top_level_domain]
    
    def load_data(self):
        if os.path.exists(OUTPUT_FILE_NAME) and os.stat(OUTPUT_FILE_NAME).st_size:
            with open(OUTPUT_FILE_NAME, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}
    
    
    def open_spider(self, spider):
        self.data: dict[str, dict[str, list]] = self.load_data()
    
    def close_spider(self, spider):
        with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=3)
    
    def process_item(self, item, spider):
        domain = spider.allowed_domains[0]
        country = self.get_country_from_domain(domain)
        
        if country not in self.data:
            self.data[country] = {}
            
        if domain not in self.data[country]:
            self.data[country][domain] = []
            
        rental_object = dict(item)
        
        if rental_object not in self.data[country][domain]:
            self.data[country][domain].append(rental_object)
            
        return item