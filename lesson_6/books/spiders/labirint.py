import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@title='Следующая']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)


    def book_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        authors = response.xpath("//div[@class='authors']/a[@data-event-label='author']/text()").getall()
        price = response.xpath("//span[contains(@class,'val-number')]/text()").getall()
        rate = response.xpath("//div[@id='rate']/text()").get()
        book_id = response.xpath("//div[@class='articul']/text()").get()
        url = response.url
        price_discount = ''
        yield BooksItem(name=name, authors=authors, price=price, url=url, rate=rate,
                        _id=book_id, price_discount=price_discount)
