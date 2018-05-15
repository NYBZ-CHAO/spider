import json
import logging
import random
from urllib.parse import urlparse

import scrapy

from kt_spider.items import KtSpiderItem

logger = logging.getLogger('kt_spider')


class JDSpider(scrapy.Spider):
    name = "kt_spider"
    rotete_user_agent = True

    def __init__(self):
        self.price_url = "https://p.3.cn/prices/mgets?pduid={}&skuIds=J_{}"
        self.price_backup_url = "https://p.3.cn/prices/get?pduid={}&skuid=J_{}"

    def start_requests(self):
        urls = [
            'https://list.jd.com/list.html?cat=737,794,870&ev=exbrand_2505&sort=sort_rank_asc&trans=1&JL=3_%E5%93%81%E7%89%8C_TCL#J_crumbsBar']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath("//@href").extract()
        for link in links:
            self.logger.debug("link: %s", link)
            url = urlparse(link)
            if url.netloc:  # 是一个 URL 而不是 "javascript:void(0)"
                if not url.scheme:
                    link = "http:" + link
                self.logger.debug("url: %s", url)
                subdomain = url.hostname.split(".")[0]
                # 如果这是一个商品，获取商品详情
                if subdomain in ["item"]:
                    yield scrapy.Request(url=link, callback=self.parse_item)

        next_page = response.xpath("//a[@class='pn-next']/@href").extract()
        if next_page:
            for next_link in next_page:
                next_link = "https://list.jd.com" + next_link
                yield scrapy.Request(url=next_link, callback=self.parse)

    def parse_item(self, response):
        if not response.text or response.text == "":
            return
        parsed = urlparse(response.url)
        item = KtSpiderItem()
        # 获取 sku_id, URL: http://item.jd.com/4297772.html 的 sku_id 就是 4297772
        item['sku_id'] = urlparse(response.url).path.split(".")[
            0].replace("/", "")
        item['brand'] = response.xpath("id('parameter-brand')/li/a[1]/text()").extract()
        names = response.xpath('//div[@class="sku-name"]/text()').extract()
        name = ''.join(str(i) for i in names).strip()
        if name == '':
            name = response.xpath("id('name')/h1/text()").extract()
        item['name'] = name
        details = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').extract()
        item['parameters'] = details
        yield scrapy.Request(url=self.price_url.format(random.randint(1, 100000000), item['sku_id']),
                             callback=self.parse_jprice,
                             meta={'item': item})

    def parse_jprice(self, response):
        item = response.meta['item']
        try:
            price = json.loads(response.text)
            item['price'] = price[0].get("p")
        except KeyError as err:
            if price['error'] == 'pdos_captcha':
                logging.error("触发验证码")
            logging.warn("Price parse error, parse is {}".format(price))
        except json.decoder.JSONDecodeError as err:
            logging.log('prase price failed, try backup price url')
            yield scrapy.Request(url=self.price_backup_url.format(random.randint(1, 100000000), item['sku_id']),
                                 callback=self.parse_price,
                                 meta={'item': item})
        yield item
