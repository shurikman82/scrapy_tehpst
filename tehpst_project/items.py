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


class TehpstFullProductItem(scrapy.Item):
    name = scrapy.Field()
    art = scrapy.Field()
    description = scrapy.Field()
#    slug = scrapy.Field()
#    country = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    brand_name = scrapy.Field()


class TehpstStockItem(scrapy.Item):
    stock_name = scrapy.Field()
    stock_quantity = scrapy.Field()
    product_art = scrapy.Field()


class TehpstPropertyItem(scrapy.Item):
    property_name = scrapy.Field()
    property_value = scrapy.Field()
    product_art = scrapy.Field()
