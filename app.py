import os
import pickle
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, render_template, request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

output = Path('./output')

app = Flask(__name__)

def decide_spider(url):
    domains = {
        'buy.housefun.com.tw': 'housefun',
        'sale.591.com.tw': '591',
        'www.591.com.tw': '591',
    }

    try:
        return domains[urlparse(url).netloc]
    except KeyError:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl_591():
    if request.method == 'POST':
        url = request.form["url"]
        spider = decide_spider(url)
        if not spider:
            return "目前只支援591跟好房網"

        if output.exists():
            os.remove(str(output))
        subprocess.run(
            ['scrapy', 'crawl', spider, '-a', f'url={url}'],
        )
        with output.open('rb') as f:
            data = pickle.load(f)
        data['url'] = url
        return render_template('results.html', data=data)
