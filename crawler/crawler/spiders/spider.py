import scrapy
from crawler.items import CrawlerItem

# class Spider(scrapy.Spider):
#     name = "GmarketBestsellers"
#     allow_domain = ["gmarket.co.kr"]
#     start_urls = ["http://corners.gmarket.co.kr/Bestsellers"]
    
#     def parse(self, response):
#         links = response.xpath('//*[@id="gBestWrap"]/div/div[3]/div[2]/ul/li/div[1]/a/@href').extract()
#         for link in links[:10]:
#             yield scrapy.Request(link, callback=self.page_content)
            
#     def page_content(self, response):
#         item = CrawlerItem()
#         item["title"] = response.xpath('//*[@id="itemcase_basic"]/h1/text()')[0].extract()
#         item["s_price"] = response.xpath('//*[@id="itemcase_basic"]/p/span/strong/text()')[0].extract().replace(",", "")
#         try:
#             item["o_price"] = response.xpath('//*[@id="itemcase_basic"]/p/span/span/text()')[0].extract().replace(",", "")
#         except:
#             item["o_price"] = item["s_price"]
#         item["discount_rate"] = str(round((1 - int(item["s_price"]) / int(item["o_price"]))*100, 2)) + "%"
#         item["link"] = response.url
#         yield item
