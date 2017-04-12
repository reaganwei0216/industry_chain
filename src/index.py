# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 23:23:56 2017

@author: tzu-ting
"""

import requests
import bs4
from .urls import root_url
from .base import base_class

class industry(base_class, dict):

    name :str

    def __init__(self, bs_item :bs4.element.Tag):
        self.name = bs_item.select_one('span.txt').text

        sub_menu = bs_item.select('li.listItem a')
        if len(sub_menu) == 0:
            self.link = bs_item.select_one('a')['href']
        else:
            for item in sub_menu:
                key = item.text.strip()
                link = item['href']
                self[key] = link

    def get_key(self):
        if len(self) == 0:
            return self.name
        else:
            return (self.name, [k for k in self])

    def get_detail(self):
        if len(self) == 0:
            return (self.name, self.link)
        else:
            return (self.name, self)

class index_page(base_class):

    def __init__(self):
        page = requests.get(root_url)
        soup = bs4.BeautifulSoup(page.content.decode('utf8'), 'lxml')

        items = soup.select('div.item') # get all item
        items = [it for it in items if 'item2' not in it.attrs['class']] # filter non-industry block

        self.items = [industry(it) for it in items]

    def get_key(self):
        return [it.get_key() for it in self.items]

    def get_detail(self):
        return dict([item.get_detail() for item in self.items])
