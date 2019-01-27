import scrapy
import re

class Spider(scrapy.Spider):
    name = 'yungching'

    def start_requests(self):
        if not hasattr(self, 'url'):
            raise RuntimeError('Please input url with -a url=<url>')
        yield scrapy.Request(getattr(self, 'url'), self.parse)

    def parse(self, response):
        self.house_info = response.css('.m-house-info-wrap')
        address = response.css('.house-info-addr::text').extract_first()

        yield {
            'title': response.css('.house-info-name::text').extract_first(),
            'house_type': self.get_house_details()[2],
            'district': address[3:6],
            'years': self.get_house_details()[1].replace('年', ''),
            'structure': self.house_info.css('.house-info-sub').css('div::text').extract()[6].strip(),
            'total_price': response.css('.price-num::text').extract_first(),
            'price_per': response.css('.m-house-detail-list.bg-price .right span::text').extract_first().strip('每坪單價約 萬'),
            'total_size': self.get_house_details()[0].strip('建物 坪'),
            'locate_floor': self.get_house_details()[3].split('~')[0],
            'max_floor': self.get_house_details()[3].split('/')[-1].replace('樓', ''),
            'main_size': response.css('.m-house-detail-list.bg-square .detail-list-lv2 li::text').extract_first().strip('主建物小計：坪'),
            'public_ratio': '',
            'manage_fee': self.manage_fee(response),
            'parking': response.css('.m-house-detail-list.bg-car li::text').extract_first() or '',
            'address': address,
        }

    def get_house_details(self):
        return self.house_info.css('.house-info-sub').css('span::text').extract()

    def manage_fee(self, response):
        data = response.css('.m-house-detail-list.bg-other.last li::text').extract()
        data = list(filter(lambda x: '管理費' in x, data))
        if not data:
            return ''
        return re.findall(r'\d+', data[0])[0]
