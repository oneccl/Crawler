
# Scrapy爬虫框架

# Scrapy是一个由Python语言开发的适用爬取网站数据、提取结构性数据的Web应用程序框架。主要用于数据挖掘、信息处理、数据存储和自动化测试等
# 通过Scrapy框架实现一个爬虫，只需要少量的代码，就能够快速的网络抓取
# Scrapy基于Twisted，Twisted是一个异步网络框架，主要用于提高爬虫的下载速度

# 官方文档：https://docs.scrapy.org
# 入门文档：https://doc.scrapy.org/en/latest/intro/tutorial.html
# 中文文档：https://www.osgeo.cn/scrapy/

# Scrapy框架5大组件（架构）
"""
1）Scrapy引擎(Scrapy Engine)：Scrapy引擎是整个框架的核心，负责Spider、ItemPipeline、Downloader、Scheduler间的通讯、数据传递等
2）调度器(Scheduler)：网页URL的优先队列，主要负责处理引擎发送的请求，并按一定方式排列调度，当引擎需要时，交还给引擎
3）下载器(Downloader)：负责下载引擎发送的所有Requests请求资源，并将其获取到的Responses交还给引擎，由引擎交给Spider来处理
4）爬虫(Spider)：用户定制的爬虫，用于从特定网页中提取信息(实体Item)，负责处理所有Responses，从中提取数据，并将需要跟进的URL提交给引擎，再次进入调度器
5）实体管道(Item Pipeline)：用于处理Spider中获取的实体，并进行后期处理（详细分析、过滤、持久化存储等）
"""
# 下载中间件(Downloader Middlewares)：一个可以自定义扩展下载功能的组件
# Spider中间件(Spider Middlewares)：一个可以自定扩展和操作引擎和Spider间通信的组件

# Scrapy环境搭建
"""
1）CMD命令行安装Scrapy：pip install scrapy
验证：scrapy
2）在存放爬虫项目的目录下创建爬虫项目：scrapy startproject ScrapyDemo
cmd下切换操作：
切盘：E:
切换目录：cd A/B/...
3）使用PyCharm打开创建的项目ScrapyDemo
4）在spiders文件夹下创建核心爬虫文件SpiderDemo.py
"""
# 最终项目结构及说明
'''
ScrapyDemo/                              爬虫项目
    ├── ScrapyDemo/                      爬虫项目目录    
    │      ├── spiders/                  爬虫文件
    │      │      ├── __init__.py   
    │      │      └── SpiderDemo.py      自定义核心功能文件
    │      ├── __init__.py   
    │      ├── items.py                  爬虫目标数据
    │      ├── middlewares.py            中间件、代理  
    │      ├── pipelines.py              管道，用于处理爬取的数据    
    │      └── settings.py               爬虫配置文件
    └── scrapy.cfg                       项目配置文件
'''
# 基本使用
'''
1）明确目标
明确爬虫的目标网站
明确需要爬取实体（属性）：items.py
定义：属性名 = scrapy.Field()
2）制作爬虫
自定义爬虫核心功能文件：spiders/SpiderDemo.py.py
3）存储数据
设计管道存储爬取内容：settings.py、pipelines.py
4）运行爬虫
方式1：在Terminal终端执行：
scrapy crawl <爬虫名>
方式2：在PyCharm执行文件
创建爬虫运行文件run.py，右键运行（像运行Python脚本一样运行爬虫）
'''

# 入门案例

# 1）明确目标
# 1.1）爬取当当网手机信息：https://category.dangdang.com/cid4004279.html


# 2）制作爬虫
import scrapy
from ..items import ScrapyDemoItem

class SpiderDemo(scrapy.Spider):
    # 爬虫名称，运行爬虫时使用的值
    name = "dangdang"
    # 爬虫域，允许访问的域名
    allowed_domains = ['category.dangdang.com']
    # 爬虫地址：起始URL：第一次访问是域名
    start_urls = ['https://category.dangdang.com/cid4004279.html']
    # 翻页分析
    # 第1页：https://category.dangdang.com/cid4004279.html
    # 第2页：https://category.dangdang.com/pg2-cid4004279.html
    # 第3页：https://category.dangdang.com/pg3-cid4004279.html
    # ......
    page = 1

    # 请求响应处理
    def parse(self, response):
        li_list = response.xpath('//ul[@id="component_47"]/li')
        for li in li_list:
            # 商品名称
            name = li.xpath('.//img/@alt').extract_first().strip()
            # print(name)
            # 商品价格
            price = li.xpath('.//p[@class="price"]/span[1]/text()').extract_first().strip()
            # print(price)
            # 获取一个实体对象就交给管道pipelines
            item = ScrapyDemoItem(name=name, price=price)
            # 封装item数据后，调用yield将控制权给管道，管道拿到item后返回该程序
            yield item
        # 每一页爬取逻辑相同，只需要将执行下一页的请求再次调用parse()方法即可
        if self.page <= 10:
            self.page += 1
            url = rf"https://category.dangdang.com/pg{str(self.page)}-cid4004279.html"
            # scrapy.Request为scrapy的请求
            # yield中断
            yield scrapy.Request(url=url, callback=self.parse)


# Response对象的属性和方法
'''
1）获取响应的字符串
response.text
2）获取响应的二进制数据
response.body
3）解析响应内容
response.xpath()
'''

