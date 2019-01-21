from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pathlib import Path
import os

process = CrawlerProcess(get_project_settings())
output = Path('./output')

if __name__ == '__main__':
    os.remove(str(output))
    process.crawl('spider', url='https://sale.591.com.tw/home/house/detail/2/5867575.html')
    process.start()
