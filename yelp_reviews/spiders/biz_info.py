# -*- coding: utf-8 -*-
import blaze as bz
import scrapy
from yelp_reviews.items import BizInfoItem


class BizInfoSpider(scrapy.Spider):
    name = "biz_info"
    # start_urls = ["http://www.yelp.com/search?find_loc=11225"]
    allowed_domains = ["yelp.com"]
    no_item_count = 0

    def start_requests(self):
        zip_path = getattr(self, 'zip_csv', 'data/nyc_zip_codes.csv')
        zips = bz.data(zip_path)
        zips = bz.compute(zips.Zip_Code)
        url_str = "https://www.yelp.com/search?find_desc=Restaurants&find_loc={}"
        urls = [url_str.format(z) for z in zips]
        self.logger.info("%s start urls for BizInfoSpider", str(len(urls)))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse_business(self, biz, response):
        try:
            biz_item = BizInfoItem()
            biz_name = biz.css('.biz-name')
            biz_item['name'] = biz_name.xpath('span/text()').extract_first()
            biz_url = biz_name.xpath('@href').extract_first()
            biz_item['url'] = response.urljoin(biz_url)
            biz_item['id'] = biz_url.split('/')[-1]
            biz_item['michelin_stars'] = 0
            biz_item['yelp_stars'] = float(biz.css('.star-img::attr(title)').extract_first().split(' ')[0])
            biz_item['style'] = ','.join(biz.css('.category-str-list a::text').extract())
            biz_item['neighborhood'] = ','.join(n.strip() for n in biz.css('.neighborhood-str-list::text').extract())
            biz_item['phone_number'] = biz.css('.biz-phone::text').extract_first().strip()

            address = biz.css('address::text').extract()
            if address:
                try:
                    biz_item['street'] = address[0].strip()
                    address = address[1].strip().split(',')
                    biz_item['city'] = address[0]
                    biz_item['state'], biz_item['zip_code'] = address[1].strip().split(' ')
                except Exception:
                    self.logger.error("Failed to parse address for %s: %s",
                                      biz_item['id'], address, exc_info=True)

            return biz_item
        except Exception as e:
            self.logger.error("Error parsing business: %s", biz_item['id'], exc_info=True)
        return None

    def parse(self, response):
        if not response.css('#logo a::text').extract_first():
            self.logger.warning('Retrying url: {}'.format(response.url))
            yield Request(url=response.url, dont_filter=True)

        businesses = response.xpath("//li[@class='regular-search-result']")

        if 'visit_captcha' in response.url:
            self.logger.warning("Captcha hit: {}".format(response.url))
            raise scrapy.exceptions.CloseSpider("Exiting spider due to captcha...")

        if not businesses:
            self.logger.warning("No businesses found in %s", str(response.url))
            if self.no_item_count == 5:
                raise scrapy.exceptions.CloseSpider("Too many pages crawled with no items, exiting...")
            self.no_item_count += 1

        for biz in businesses:
            biz_item = self.parse_business(biz, response)
            if biz_item:
                yield biz_item

        next_url = response.css('a.next::attr(href)').extract_first()
        if next_url:
            next_page = response.urljoin(next_url)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
