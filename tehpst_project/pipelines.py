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
    async_engine = create_async_engine(ASYNC_CONNECTION_STRING)
    async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession)
    AsyncLocalSession = async_scoped_session(session_factory=async_session_factory, scopefunc=lambda: None)

    def open_spider(self, spider):
        engine = create_engine(CONNECTION_STRING)
#        async_engine = create_async_engine(ASYNC_CONNECTION_STRING)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
#        async_engine = create_async_engine(ASYNC_CONNECTION_STRING)
#        async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession)
#        AsyncLocalSession = async_scoped_session(session_factory=async_session_factory, scopefunc=lambda: spider)
#        self.session = AsyncSession(engine)
#        async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession)
#        AsyncLocalSession = async_scoped_session(session_factory=async_session_factory)
#        self.session = Session(engine)

    async def process_item(self, item, spider):
        if spider.name == 'tehpst_products':
            adapter = ItemAdapter(item)
            product_url = ProductUrl(url=adapter['href'], product_name=adapter['product_name'])
#            async with self.AsyncLocalSession() as session:
            self.session = self.AsyncLocalSession()
            self.session.add(product_url)
#            await self.AsyncLocalSession.commit()
#            await self.session.flush()
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()


    async def get_async_session(self):
        async_engine = create_async_engine(ASYNC_CONNECTION_STRING)
        async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession)
        AsyncLocalSession = async_scoped_session(session_factory=async_session_factory)
        yield AsyncLocalSession