"""
@author: tzing
@create: Apr 13, 2017
"""
from .base import base_class
import requests
import bs4
from urllib.parse import urljoin

root_url = r'http://ic.tpex.org.tw/introduce.php'

def get_url(id):
    return f'{root_url}?ic={id}'

class industry_chain(base_class):
    def __init__(self, url, id=None):
        if id is not None:
            url = get_url(id)
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content.decode('utf8'), 'lxml')

        self.name = soup.select_one('h3').text

        panel_main = soup.select_one('div#main_ic_panel')

        # type A - contains chain info
        if panel_main.select_one(chain.pat.frame):
            for chain_soup in panel_main.select(chain.pat.frame):
                self.append(chain(chain_soup, soup))

        # type B - no chain contains
        else:
            for group_soup in panel_main.select(idv_group.pat.frame):
                self.append(idv_group(group_soup, soup))

class chain(base_class): # chain panel: 上游/中游/下游
    class pat:
        frame = 'div.chain'
        name = 'div.chain-title-panel'

    def __init__(self, chain_soup, page_soup):
        self.name = chain_soup.select_one(self.pat.name).text

        for group_soup in chain_soup.select(group.pat.frame):
            self.append(group(group_soup, page_soup))

class group(base_class): # group (button-like): 子產業
    class pat:
        frame = 'div.company-chain-panel'

    def __init__(self, group_soup, page_soup):
        self.name = group_soup.text
        self.id = group_soup['id'].split('_')[2] # originally `ic_link_XXX`

        window_soup = page_soup.select_one(f'div#companyList_{self.id}')

        # type A.1 - conatins subchain
        if window_soup.select_one(sub_chain.pat.frame):
            sub_chains = window_soup.select(sub_chain.pat.frame)
            sub_chains.extend(window_soup.select(sub_chain.pat.frame2))
            for sc in sub_chains:
                self.append(sub_chain(sc, page_soup))

        # type A.2 - show table directly
        else:
            company.append_to(self, self.id, page_soup)

class sub_chain(base_class): # sub_chain: 子產業鏈 e.g.半導體產業 > IC製造
    class pat:
        frame = 'div.subchain'
        frame2 = 'div.subchain-hover'

    def __init__(self, chain_soup, page_soup):
        self.name = chain_soup.text.strip()
        self.id = chain_soup['id'].split('_')[2] # originally `sc_link_XXX`

        company.append_to(self, self.id, page_soup)

class company(base_class): # company: 公司

    @staticmethod
    def append_to(parent, id, page_soup):
        table = page_soup.select_one(f'table#sc_company_{id}')
        if table is None:
            table = page_soup.select_one(f'div#companyList_{id}')

        for com in table.select('a.company-text-over'):
            parent.append(company(com))

    def __init__(self, soup):
        self.name = soup.text
        self.link = urljoin(root_url, soup['href'])
        if self.link.find('stk_code=') > -1:
            self.id = self.link[self.link.find('=')+1:]

class idv_group(base_class): # 獨立子產業 e.g. 金融 / 下各類無上下游關聯
    class pat:
        frame = 'div.company-chain-panel2'

    def __init__(self, group_soup, page_soup):
        self.name = group_soup.text
        self.id = group_soup['id'].split('_')[2] # originally `ic_link_U400`

        company.append_to(self, self.id, page_soup)
