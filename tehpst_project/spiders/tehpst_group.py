import scrapy

from tehpst_project.items import TehpstGroupItem


class TehpstGroupSpider(scrapy.Spider):
    name = "tehpst_group"
    allowed_domains = ["tehpst.site"]
    start_urls = ["https://tehpst.site/products/"]

    def parse(self, response):
        for group in response.css('ul.submenu-item'):
            groups = group.css('a::text').getall()
            hrefs = group.css('a::attr(href)').getall()
            for group, href in zip(groups, hrefs):
                data = {
                    'group': group,
                    'href': 'https://tehpst.site' + href,
                }
                yield TehpstGroupItem(data)
