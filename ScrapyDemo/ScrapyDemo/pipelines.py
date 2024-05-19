# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 3）存储数据
# 3.2）使用管道存储数据
# 若使用管道，则必须在settings.py中开启管道

import csv

# 爬取网页
class ScrapyDemoPipeline(object):

    def open_spider(self, spider):
        # 在爬虫开启的时候仅执行一次
        pass

    # 数据item交给管道输出
    def process_item(self, item, spider):
        print(item)
        return item

    def close_spider(self, spider):
        # 在爬虫关闭的时候仅执行一次
        pass


# 保存数据
class ScrapyDemoSinkPiepline(object):

    # 在爬虫开启的时候仅执行一次
    def open_spider(self, spider):
        # 写入表头仅执行一次
        with open(r'C:\Users\cc\Desktop\scrapy_res.csv', 'w', newline='', encoding='utf-8') as csvfile:
            # 定义表头
            fields = ['name', 'price']
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()

    # item为yield后面的ScrapyDemoItem对象，字典类型
    def process_item(self, item, spider):
        with open(r'C:\Users\cc\Desktop\scrapy_res.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # 追加写入数据
            # ※ csv模块：字典追加写入的是Key，需要转换为List或Tuple类型(即Value) ※
            writer.writerow(list(item.values()))

    def close_spider(self, spider):
        # 在爬虫关闭的时候仅执行一次
        pass



