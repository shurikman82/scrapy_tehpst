# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from slugify import slugify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from tehpst_project.constants import ASYNC_CONNECTION_STRING, CONNECTION_STRING
from tehpst_project.models import Base, ProductUrl, FullProduct, Stocks, Product_property
from tehpst_project.items import TehpstFullProductItem


class TehpstProjectPipeline:
    def __init__(self):
        self.class_names = set()
        self.hrefs = set()
        self.arts = set()
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if spider.name == 'tehpst_products':
            if adapter['href'] in self.hrefs:
                raise DropItem(f'Dublicate item found: {item!r}')
            else:
                self.hrefs.add(adapter['href'])
                return item
        if spider.name == 'tehpst_full_products':
            if isinstance(item, TehpstFullProductItem):
                if adapter['art'] in self.arts:
                    raise DropItem(f'Dublicate art found: {item!r}')
                else:
                    self.arts.add(adapter['art'])
                    return item
            else:
                return item
        if not adapter.get('class_name'):
            return item
        else:
            if adapter['class_name'] in self.class_names:
                raise DropItem(f'Dublicate item found: {item!r}')
            else:
                self.class_names.add(adapter['class_name'])
                return item


class TehpstToDBPipeline:
    def open_spider(self, spider):
        if spider.name == 'tehpst_products':
            engine = create_engine(CONNECTION_STRING)
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            self.session = Session(engine)
        if spider.name == 'tehpst_full_products':
            engine = create_engine(CONNECTION_STRING)
#            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            self.session = Session(engine)

    def process_item(self, item, spider):
        if spider.name == 'tehpst_products':
            adapter = ItemAdapter(item)
            product_url = ProductUrl(url=adapter['href'], product_name=adapter['product_name'])
            self.session.add(product_url)
            self.session.commit()
            return item
        if spider.name == 'tehpst_full_products':
            adapter = ItemAdapter(item)
            if adapter.get('name'):
                product = FullProduct(
                    name=adapter['name'],
                    art=adapter['art'],
                    brand_name=adapter['brand_name'],
                    quantity=int(adapter['quantity']),
                    price=float(adapter['price']),
                    description=adapter['description'],
                )
                self.session.add(product)
                self.session.flush()
                product_id = product.id
                product.slug = slugify(adapter['name']) + '-' + str(product_id)
                self.session.commit()
                return item
            if adapter.get('stock_name'):
                product_art = adapter['product_art']
                product_id = self.session.execute(select(FullProduct.id).filter_by(art=product_art)).scalar_one()
                stock = Stocks(
                    stock_name=adapter['stock_name'],
                    stock_quantity=int(adapter['stock_quantity']),
                    product_id=product_id,
                )
                self.session.add(stock)
                return item
            if adapter.get('property_name'):
                product_art = adapter['product_art']
                product_id = self.session.execute(select(FullProduct.id).filter_by(art=product_art)).scalar_one()
                property = Product_property(
                    property_name=adapter['property_name'],
                    property_value=adapter['property_value'],
                    product_id=product_id,
                )
                self.session.add(property)
                self.session.commit()
                return item

    def close_spider(self, spider):
        if spider.name == 'tehpst_products':
            self.session.close()
        if spider.name == 'tehpst_full_products':
            self.session.close()
