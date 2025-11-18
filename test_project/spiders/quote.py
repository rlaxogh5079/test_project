import scrapy
from test_project.items import QuoteItem


class QuoteSpider(scrapy.Spider):
    name = "quote"
    
    def start_requests(self):
        urls = [f"https://quotes.toscrape.com/page/{i}/" for i in range(1, 11)] # 1페이지부터 10페이지 까지 크롤링
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        target_data = response.xpath("//div[@class='row']/div[@class='col-md-8']/div[@class='quote']") # col-md-8 내부에 있는 quote 요소 모두 불러오기
        
        for i in range(10): # 한 페이지당 아이템이 10개 존재
      # for i in range(len(target_data)) 또한 가능
            item = QuoteItem()
            item["quote"] =  target_data[i].xpath("span[1]/text()").get()[1:-2] # quote를 불러오고 양 끝의 쌍따옴표("") 제거
            item["name"] = target_data[i].xpath("span[2]/small/text()").get() # quote를 언급한 사람의 이름 불러오기
            item["tags"] = target_data[i].xpath("div[@class='tags']/a/text()").getall() # tags 텍스트 모두 불러오기
            yield item