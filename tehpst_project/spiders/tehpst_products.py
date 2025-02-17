import json
import scrapy

from tehpst_project.items import TehpstProductItem


class TehpstProductsSpider(scrapy.Spider):
    name = "tehpst_products"
    allowed_domains = ["tehpst.site"]
    start_urls = []
    try:
        with open('classes.json', 'r') as f:
            classes = json.load(f)
        for class_ in classes:
            start_urls.append(class_['href'])
    except Exception:
        print('file "classes.json" is empty')

    def parse(self, response):
        my_div = response.css('div.tab-pane.show.active.clearfix')
        for product in my_div.css(
                'div.product__box.product__box--default.product__box--border-hover.text-center.float-left.float-3.etimclass'
            ):

            data = {
                'product_name': product.css('a.product__link.product__link--underline.product__link--weight-light.m-t-15::text').get().strip(),
                'href': 'https://tehpst.site' + product.css('a::attr(href)').get(),
            }
            yield TehpstProductItem(data)
        next_page = None
        next_page_links = response.css('a.page-pagination__link.btn.btn--gray')
        if next_page_links:
            for link in next_page_links:
                if 'Следующая' in link.css('::text').get():
                    next_page = link
        if next_page:
            next_page_link = next_page.css('a::attr(href)').get()
            yield response.follow(
                url=next_page_link,
                callback=self.parse,
            )