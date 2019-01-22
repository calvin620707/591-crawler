import scrapy

class Spider(scrapy.Spider):
    name = '591'

    def start_requests(self):
        if not hasattr(self, 'url'):
            raise RuntimeError('Please input url with -a url=<url>')
        yield scrapy.Request(getattr(self, 'url'), self.parse)

    def parse(self, response):
        self.addr_items = response.css('.info-addr-content')
        self.house_details = response.css('.detail-house-item')

        address = self._find_addr('地址')
        floor = self._find_addr('樓層')
        locate_floor, max_floor = floor.replace('F', '').split('/')

        yield {
            'title': response.css('.detail-title-content::text').extract_first().replace(' ', '').replace('\n', ''),
            'house_type': self._get_house_detail('型態'),
            'district': address[3:6],
            'years': response.css('.info-floor-key::text')[1].extract().replace('年', ''),
            'structure': response.css('.info-floor-key::text')[0].extract(),
            'total_price': response.css('.info-price-num::text')[0].extract(),
            'price_per': response.css('.info-price-per::text')[0].extract().replace('萬/坪', ''),
            'total_size': response.css('.info-floor-key::text')[2].extract().replace('坪', ''),
            'locate_floor': locate_floor,
            'max_floor': max_floor,
            'main_size': self._get_house_detail('主建物').replace('坪', ''),
            'public_ratio': self._get_house_detail('公設比'),
            'manage_fee': self._get_house_detail('管理費').replace('元', ''),
            'parking': self._get_house_detail('車位').replace('無', ''),
            'address': address,
        }

    def _get_house_detail(self, key):
        for item in self.house_details:
            if item.css('.detail-house-key::text').extract_first() == key:
                return item.css('.detail-house-value::text').extract_first()
        return ''

    def _find_addr(self, key):
        for item in self.addr_items:
            if item.css('.info-addr-key::text').extract_first() == key:
                return item.css('.info-addr-value::text').extract_first()