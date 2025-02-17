import scrapy
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from tehpst_project.constants import CONNECTION_STRING
from tehpst_project.items import TehpstFullProductItem
from tehpst_project.models import Base, ProductUrl


class TehpstFullProductsSpider(scrapy.Spider):
    name = "tehpst_full_products"
    allowed_domains = ["tehpst.site"]
    start_urls = []
    engine = create_engine(CONNECTION_STRING)
    session = Session(engine)
    try:
        all_url = session.execute(select(ProductUrl.url))
        for url in all_url.scalars():
            start_urls.append(url)
    except Exception:
        print('Table "productrl" is empty')


    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set('DOWNLOAD_DELAY', '0.1', priority='spider')


    def parse(self, response):
        my_div = response.css('main.main-container').css('div.product-details-box')
        values = my_div.css('h5::text').getall()
        print(values)
        name, art, brand_name, quantity = values[0], values[1].strip().split()[-1], values[2], values[3].strip().split()[-1]
        if quantity == 'наличие':
            quantity = '0'
        div_2 = response.css('main.main-container').css('div.product__price')
        price = div_2.css('span::text').get()
        price_clean = price.strip().split()[0].replace(',', '.')
        if price_clean == 'Цена':
            price_clean = '0'
        div_3 = response.css('main.main-container').css('div.product__desc.m-t-25.m-b-30')
        description = div_3.css('p::text').get()
        
        div_4 = response.css('main.main-container').css('div.product__desc.m-t-25.m-b-3').css('table.table')
        stocks = div_4.css('tr.table-light')
        stocks = stocks[1:]
        stocks_list = []
        for stock in stocks:
            stock_name, stock_quantity = stock.css('td::text').getall()
            stock_data = {
                'stock_name': stock_name,
                'stock_quantity': stock_quantity,
            }
            stocks_list.append(stock_data)
        my_div_2 = response.css('div.product.product--1.border-around.product-details-tab-area').css('div.tab-pane.show.active')
        properties = my_div_2.css('table.product-dis__list.table.table-bordered').css('tr')
        properties_list = []
        for property in properties:
            property_name = property.css('td.product-dis__title::text').get()
            property_value = property.css('td.product-dis__text::text').get()
            property_data = {
                'property_name': property_name,
                'property_value': property_value,
            }
            properties_list.append(property_data)
        product_data = {
            'name': name,
            'art': art,
            'brand_name': brand_name,
            'quantity': quantity,
            'price': price_clean,
            'description': description,
            'stocks': stocks_list,
            'properties': properties_list
        }
        yield TehpstFullProductItem(product_data)

