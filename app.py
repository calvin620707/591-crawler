import os
from pathlib import Path
import pickle

from flask import Flask, render_template, request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import subprocess

output = Path('./output')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/591', methods=['POST'])
def crawl_591():
    if request.method == 'POST':
        url = request.form["url"]
        if 'sale.591.com.tw' not in url and 'www.591.com.tw' not in url:
            return "請輸入591網址"

        if output.exists():
            os.remove(str(output))
        subprocess.run(
            ['scrapy', 'crawl', 'spider', '-a', f'url={url}'],
        )
        with output.open('rb') as f:
            data = pickle.load(f)
        data['url'] = url
        return render_template('591_results.html', data=data)
