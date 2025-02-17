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
    quantity = scrapy.Field()
    price = scrapy.Field()
    brand_name = scrapy.Field()
    stocks = scrapy.Field()
    properties = scrapy.Field()
