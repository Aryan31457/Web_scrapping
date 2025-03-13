import scrapy
from scrapy_playwright.page import PageMethod

import random


class GoatSpider(scrapy.Spider):
    name = "goatspider"
    allowed_domains = ["www.goat.com"]
    start_urls = ["https://www.goat.com/sneakers"]
    max_pages = 50  

    
    proxies = [
        "http://3.94.143.61:3128",
        "http://13.38.153.36:80",
        "http://13.37.89.201:80",
        "http://13.37.59.99:3128",
        "http://13.38.176.104:3128",
    ]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        },
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_selector", 'div[data-qa="grid_cell_product"]'),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                ],
                "proxy": random.choice(self.proxies), 
                "page": 1,
            },
            dont_filter=True
        )

    async def parse(self, response):
        base_url = "https://www.goat.com"

        for product in response.css('div[data-qa="grid_cell_product"]'):
            relative_href = product.css('a::attr(href)').get()
            full_href = base_url + relative_href if relative_href else None

            yield {
                "name": product.css('a::attr(aria-label)').get(),
                "href": full_href,
            }

        current_page = response.meta.get("page", 1)
        if current_page < self.max_pages:
            next_page = current_page + 1
            yield scrapy.Request(
                url=self.start_urls[0],
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", 'div[data-qa="grid_cell_product"]'),
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    ],
                    "proxy": random.choice(self.proxies), 
                    "page": next_page,
                },
                dont_filter=True
            )

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)")],
                "page": 1
            },
        )

    def parse(self, response):
        base_url = "https://www.goat.com"

        for product in response.css('div[data-qa="grid_cell_product"]'):
            relative_href = product.css('a::attr(href)').get()
            full_href = base_url + relative_href if relative_href else None

            yield {
                "name": product.css('a::attr(aria-label)').get(),
                "href": full_href
            }

        current_page = response.meta.get("page", 1)
        if current_page < self.max_pages:
            next_page = current_page + 1
            yield scrapy.Request(
                url=self.start_urls[0],
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)")],
                    "page": next_page
                },
                dont_filter=True
            )