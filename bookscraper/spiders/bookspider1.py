import scrapy


class Bookspider1Spider(scrapy.Spider):
    name = "bookspider1"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books=response.css('article.product_pod')

        for book in books:

            next_book=response.css('li.next a::attr(href)').get()

            if 'catalogue/' in next_book:
                next_book_url='https://books.toscrape.com/'+next_book
            else:
                next_book_url='https://books.toscrape.com/catalogue/'+next_book

            yield response.follow(next_book_url ,callback=self.parse_book_page)


    def parse_book_page(self,response):
            
            books=response.css('article.product_pod')
            for book in books:
                yield {
                'name':book.css('h3 a::text').get(),
                'price':book.css('product_price .price_color::text').get(),
                'url':book.css('h3 a').attrib['href']
                }
