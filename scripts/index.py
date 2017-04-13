from .base import base_class
from .chain import industry_chain
from os import path
import requests
import bs4

root_url = r'http://ic.tpex.org.tw/'

def solve_link(link :str):
    fulllnk = path.join(root_url, link)
    page_id = link[link.find('=')+1:]
    return fulllnk, page_id

class industry(base_class):
    def __init__(self, item :bs4.element.Tag):
        self.name = item.select_one('span.txt').text

        sub_menu = item.select('li.listItem a')
        if len(sub_menu) == 0:
            self.link, self.id = solve_link(item.select_one('a')['href'])
            return

        for item in sub_menu:
            self.append(sub_industry(item))

    def fire_query(self) -> industry_chain:
        if self.link is None:
            raise RuntimeError('not a quariable object')
        return industry_chain(self.link)

class sub_industry(industry):
    def __init__(self, item):
        self.name = item.text.strip()
        self.link, self.id = solve_link(item['href'])

class index(base_class):
    def __init__(self):
        page = requests.get(root_url)
        soup = bs4.BeautifulSoup(page.content.decode('utf8'), 'lxml')

        # filter non-industry block
        items = [it for it in soup.select('div.item') if 'item2' not in it.attrs['class']]

        # output
        self['name'] = '產業鍊價值資訊平台'
        self['link'] = root_url
        for item in items:
            self.append(industry(item))
