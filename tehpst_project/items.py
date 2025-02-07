# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TehpstGroupItem(scrapy.Item):
    group = scrapy.Field()
    href = scrapy.Field()


class TehpstClassItem(scrapy.Item):
    class_name = scrapy.Field()
    href = scrapy.Field()


class TehpstProductItem(scrapy.Item):
    product_name = scrapy.Field()
    href = scrapy.Field()
