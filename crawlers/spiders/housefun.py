import scrapy

class Spider(scrapy.Spider):
    name = 'housefun'

    def start_requests(self):
        if not hasattr(self, 'url'):
            raise RuntimeError('Please input url with -a url=<url>')
        yield scrapy.Request(getattr(self, 'url'), self.parse)

    def parse(self, response):
        self.extra_info = response.css('.extra-info span.desc::text')
        self.info_sub = response.css('.info-sub>li::text')
        address = self._get_extra_info(0)
        floor = self._get_extra_info(1).split('~')[1].strip()
        locate_floor, max_floor = floor.split('/')

        size_info = self._get_info_sub(1)
        total_size = size_info.split('(')[0].strip('總坪數 坪')

        yield {
            'title': response.css('.main>.heading::text').extract_first(),
            'house_type': self._get_extra_info(4).split('/')[0],
            'district': address[3:6],
            'years': self._find_extra_info('屋齡').strip('屋齡年 '),
            'structure': self._get_info_sub(0),
            'total_price': response.css('#total-amount::text').extract_first().replace(',', ''),
            'price_per': self._get_info_sub(2).strip('單價萬/坪 單價含車位單價計算方式請洽業務'),
            'total_size': total_size,
            'locate_floor': locate_floor,
            'max_floor': max_floor,
            'main_size': response.css('.popover-content .info::text')[0].extract().strip(' 坪'),
            'public_ratio': '',
            'manage_fee': self._find_extra_info('管理費').strip('管理費 元/月').replace(',', ''),
            'parking': self._find_extra_info('車位', exclude='輪椅'),
            'address': address,
        }

    def _get_extra_info(self, index):
        try:
            return self.extra_info[index].extract()
        except:
            return ''

    def _find_extra_info(self, keyword, exclude=''):
        for item in self.extra_info:
            text = item.extract()
            if keyword in text and exclude not in text:
                return text
        return ''

    def _get_info_sub(self, index):
        try:
            return self.info_sub[index].extract()
        except:
            return ''