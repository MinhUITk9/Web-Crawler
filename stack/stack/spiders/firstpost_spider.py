from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem
import scrapy

class Firstpost(Spider):
    name = "firstpost"
    start_urls = ["http://www.firstpost.com/tech/reviews",
                "http://www.firstpost.com/tech/reviews/page/2",
                "http://www.firstpost.com/tech/reviews/page/3",
                "http://www.firstpost.com/tech/reviews/page/4",
                "http://www.firstpost.com/tech/reviews/page/5",
                "http://www.firstpost.com/tech/reviews/page/6",
                "http://www.firstpost.com/tech/reviews/page/7",
                "http://www.firstpost.com/tech/reviews/page/8",
                "http://www.firstpost.com/tech/reviews/page/9",
                "http://www.firstpost.com/tech/reviews/page/10",
                "http://www.firstpost.com/tech/reviews/page/11"]

    def parse(self, response):
        questions = Selector(response).xpath('//a[@class="list-item-link"]')

        for question in questions:
            item= StackItem()
            url = question.xpath('@href').extract()[0]
            item['url'] = question.xpath('@href').extract()[0]
            item['title'] = question.xpath('div[@class="info-wrap"]/p[@class="list-title"]/text()').extract()[0]
            item['desc'] = question.xpath('div[@class="info-wrap"]/div[@class="list-desc"]/text()').extract()[0]
            request = scrapy.Request(url, callback = self.parse_content)
            request.meta['item'] = item
            yield request
    
    def parse_content(self,response):
        item = response.meta['item']
        content = Selector(response).xpath('//div[@class="container article"]')
        item['body'] = content.xpath('h1[@class="page-title article-title"]/text()').extract()[0]
        yield item
