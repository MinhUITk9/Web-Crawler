from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem

class Firstpost(Spider):
    name = "firstpost"
    allowed_domains = ["http://www.firstpost.com"]
    start_urls = ["http://www.firstpost.com/tech/reviews"]

    def parse(self, response):
        questions = Selector(response).xpath('//a[@class="list-item-link"]')

        for question in questions:
            item= StackItem()
            item['url'] = question.xpath('@href').extract()[0]
            item['title'] = question.xpath('div[@class="info-wrap"]/p[@class="list-title"]/text()').extract()[0]
            yield item