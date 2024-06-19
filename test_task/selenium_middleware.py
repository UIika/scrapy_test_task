from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--log-level=3') 
        self.driver = webdriver.Chrome(options=chrome_options)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(2)
        body = self.driver.page_source
        url = self.driver.current_url
        return HtmlResponse(
            url, body=body, encoding='utf-8', request=request
        )
    
    def __del__(self):
        self.driver.quit()