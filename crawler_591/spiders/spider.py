import scrapy

class Spider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        if not hasattr(self, 'url'):
            raise RuntimeError('Please input url with -a url=<url>')
        yield scrapy.Request(getattr(self, 'url'), self.parse)

    def parse(self, response):
        self.addr_items = response.css('.info-addr-content')
        address = self._find_addr()
        floor = self.addr_items[0].css('.info-addr-value::text').extract_first()
        locate_floor, max_floor = floor.replace('F', '').split('/')
        self.house_details = response.css('.detail-house-value::text')

        yield {
            'title': response.css('.detail-title-content::text').extract_first().replace(' ', '').replace('\n', ''),
            'house_type': self._get_detail(1),
            'district': address[3:6],
            'years': response.css('.info-floor-key::text')[1].extract().replace('年', ''),
            'structure': response.css('.info-floor-key::text')[0].extract(),
            'total_price': response.css('.info-price-num::text')[0].extract(),
            'price_per': response.css('.info-price-per::text')[0].extract().replace('萬/坪', ''),
            'total_size': response.css('.info-floor-key::text')[2].extract().replace('坪', ''),
            'locate_floor': locate_floor,
            'max_floor': max_floor,
            'main_size': self._get_detail(8).replace('坪', ''),
            'public_ratio': self._get_detail(7),
            'manage_fee': self._get_detail(3).replace('元', ''),
            'parking': self._get_detail(6).replace('無', ''),
            'address': address,
        }

    def _get_detail(self, index):
        return self.house_details[index].extract() if len(self.house_details) > index else ''

    def _find_addr(self):
        for item in self.addr_items:
            if item.css('.info-addr-key::text').extract_first() == '地址':
                return item.css('.info-addr-value::text').extract_first()