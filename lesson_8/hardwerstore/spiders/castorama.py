import scrapy
from scrapy.http import HtmlResponse
from hardwerstore.items import HardwerstoreItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class,'product-card__name')]")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=HardwerstoreItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//div[contains(@class,'add-to-cart__price')]//"
                                  "div[@class='current-price']//span[@class='price']//text()")
        loader.add_xpath('photos', "//img[contains(@class,'top-slide__img')]/@data-src")
        loader.add_xpath('_id', "//span[@itemprop='sku']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('spec_name', "//div[contains(@class,'product-specifications')]"
                                      "//dl/dt/span[contains(@class, 'specs-table__attribute-name')]//text()")
        loader.add_xpath('spec_value', "//div[contains(@class,'product-specifications')]//dl/dd//text()")
        yield loader.load_item()
