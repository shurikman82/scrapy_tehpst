# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, async_scoped_session, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tehpst_project.constants import ASYNC_CONNECTION_STRING, CONNECTION_STRING
from tehpst_project.models import Base, ProductUrl


class TehpstProjectPipeline:
    def __init__(self):
        self.class_names = set()
        self.hrefs = set()
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if spider.name == 'tehpst_products':
            if adapter['href'] in self.hrefs:
                raise DropItem(f'Dublicate item found: {item!r}')
            else:
                self.hrefs.add(adapter['href'])
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
#    def __init__(self):
#        self.create_async_connection()
    
    def create_async_connection(self):
        self.async_engine = create_async_engine(ASYNC_CONNECTION_STRING)
#        self.async_session_factory = async_sessionmaker(bind=self.async_engine, class_=AsyncSession)
#        self.AsyncLocalSession = async_scoped_session(session_factory=self.async_session_factory, scopefunc=lambda: None)
#        self.session = self.AsyncLocalSession()
#        self.async_session = AsyncSession(self.async_engine)

    def open_spider(self, spider):
        engine = create_engine(CONNECTION_STRING)
#        async_engine = create_async_engine(ASYNC_CONNECTION_STRING)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
#        self.async_session = AsyncSession(self.async_engine)
        async_engine = create_async_engine(ASYNC_CONNECTION_STRING)
#        async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession)
#        AsyncLocalSession = async_scoped_session(session_factory=async_session_factory, scopefunc=lambda: spider)
        self.async_session = AsyncSession(async_engine)
#        async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession)
#        AsyncLocalSession = async_scoped_session(session_factory=async_session_factory)
#        self.session = Session(engine)

    def insert_in_base(self, obj):
        self.async_session.add(obj)
        self.async_session.commit()


    def process_item(self, item, spider):
        if spider.name == 'tehpst_products':
            adapter = ItemAdapter(item)
            product_url = ProductUrl(url=adapter['href'], product_name=adapter['product_name'])
            self.async_session.add(product_url)
#            self.insert_in_base(product_url)
            self.async_session.commit()
#            await session.close()
#            self.session = self.Session()
#            self.session.add(product_url)
#            await self.AsyncLocalSession.commit()
#            await self.session.flush()
            return item

    def close_spider(self, spider):
        self.async_session.commit()
        self.async_session.close()
