# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 1）明确目标
# 1.2）明确需要爬取实体属性
class ScrapyDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品名称
    name = scrapy.Field()
    # 商品价格
    price = scrapy.Field()


