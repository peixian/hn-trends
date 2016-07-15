
#HN uses the https://news.ycombinator.com/front?day={yyyy}-{mm}-{dd} format for top posts of that day

import requests
from bs4 import BeautifulSoup as bs
from datetime import date, datetime, timedelta
import pandas as pd
import re
import html2text
import numpy as np

class Scrape(object):

    def __init__(self):
        self.url_base = 'https://news.ycombinator.com/front'
        self.url = 'https://news.ycombinator.com/'

    def return_comments_page(self, item_url):
        req = requests.get(self.url+item_url)
        soup = bs(req.content, 'html.parser')
        comments = list(map(lambda x: x.text.strip(), soup.find_all(class_='comment')))
        comments = np.array(comments)
        return comments

    def return_comments_date(self, date):
        #returns the comments for a particular day as a list
        params = {'day': date.strftime('%Y-%m-%d')}
        req = requests.get(self.url_base, params)
        content = html2text.html2text(str(req.content))
        comment_links = list(set(re.findall('item\?id=[0-9]*', content)))
        comments = list(map(lambda x: self.return_comments_page(x), comment_links))
        comments = np.array(comments)
        return comments

    def return_comments_range(self, start_date, end_date):
        #returns all the comments for a range of dates
        date_range = pd.date_range(start_date, end_date)
        comments = list(map(lambda x: self.return_comments(x), date_range))
        comments = np.array(comments)
        return comments


