from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem
import scrapy

class Firstpost(Spider):
    name = "firstpost"
    # url = ""
    # title = ""
    # desc = ""
    body = ""
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
        item = StackItem()
        url = str(response)[5:-1]
        item['url'] = url
        try:
            if url not in self.start_urls:
                content = Selector(response).xpath('//div[@class="container article"]')
                item['body'] = content.xpath('h1[@class="page-title article-title"]/text()').extract()[0]
                yield item

            questions = Selector(response).xpath('//a[@class="list-item-link"]')
            for question in questions:
                question_url = question.xpath('@href').extract()[0]   
                for sub_item in self.parse(question_url):
                    sub_item['title'] = question.xpath('div[@class="info-wrap"]/p[@class="list-title"]/text()').extract()[0]
                    sub_item['desc'] = question.xpath('div[@class="info-wrap"]/div[@class="list-desc"]/text()').extract()[0]
                    yield sub_item

        except Exception as e:
            import traceback
            item['exception'] = str(e)
            item['traceback'] = traceback.format_exc()
        yield item
            
            #yield scrapy.Request(response.urljoin(url_link), callback=self.parse_nextpage)
            # global body
            # body = ""
            #yield item
            #yield scrapy.Request(response.urljoin(url_link), callback=self.parse_nextpage)
            #yield item
            #yield scrapy.Request(response.urljoin(url_link), callback=self.parse_nextpage)
            #item['body'] = body
            #yield item
    
    # def parse_nextpage(self, response):
    #         content = Selector(response).xpath('//div[@class="container article"]')
    #         item
    #         item['body'] = content.xpath('h1[@class="page-title article-title"]/text()').extract()[0]
    #         yield item
            
            
