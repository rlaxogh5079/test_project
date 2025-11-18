# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    quote = scrapy.Field() # 명언 필드
    name = scrapy.Field() # 이름 필드
    tags = scrapy.Field() # 태그 필드