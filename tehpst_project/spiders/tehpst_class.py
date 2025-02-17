import json
import scrapy

from tehpst_project.items import TehpstClassItem


class TehpstClassSpider(scrapy.Spider):
    name = "tehpst_class"
    allowed_domains = ["tehpst.site"]
    start_urls = []
    try:
        with open('groups.json', 'r') as f:
            groups = json.load(f)
        for group in groups:
            start_urls.append(group['href'])
    except Exception:
        print('file "groups.json" is empty')

    def parse(self, response):
        for class_ in response.css('div.tab-pane.show.active.clearfix'):
            divs = class_.css('div.product__box.product__box--default.product__box--border-hover.text-center.float-left.float-4')
            for div in divs:
                data = {
                    'class_name': div.css('a::text').get().strip(),
                    'href': 'https://tehpst.site' + div.css('a::attr(href)').get(),
                }
                yield TehpstClassItem(data)
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
