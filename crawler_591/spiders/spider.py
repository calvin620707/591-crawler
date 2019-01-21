import scrapy

class Spider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        if not hasattr(self, 'url'):
            raise RuntimeError('Please input url with -a url=<url>')
        yield scrapy.Request(getattr(self, 'url'), self.parse)

    def parse(self, response):
        # house_type = response.css('.detail-house-value::text')[1].extract()
        address = response.css('.info-addr-value::text')[2].extract()
        floor = response.css('.info-addr-value::text')[0].extract()
        locate_floor, max_floor = floor.replace('F', '').split('/')

        yield {
            'title': response.css('.detail-title-content::text').extract_first().replace(' ', '').replace('\n', ''),
            'district': address[3:6],
            'years': response.css('.info-floor-key::text')[1].extract().replace('年', ''),
            'structure': response.css('.info-floor-key::text')[0].extract(),
            'total_price': response.css('.info-price-num::text')[0].extract(),
            'price_per': response.css('.info-price-per::text')[0].extract().replace('萬/坪', ''),
            'total_size': response.css('.info-floor-key::text')[2].extract().replace('坪', ''),
            'locate_floor': locate_floor,
            'max_floor': max_floor,
            'main_size': response.css('.detail-house-value::text')[8].extract().replace('坪', ''),
            'public_ratio': response.css('.detail-house-value::text')[7].extract(),
            'manage_fee': response.css('.detail-house-value::text')[3].extract().replace('元', ''),
            'parking': response.css('.detail-house-value::text')[6].extract().replace('無', ''),
            'address': address,
        }