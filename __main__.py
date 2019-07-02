import os
import ssl
import sys
import time
from datetime import datetime
from itertools import count
from urllib.request import Request, urlopen
# import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler

def crawling_pelicana():
    results = []

    for page in count(start=113):  # 처음만 지정하는것 꼭 break가 있어야함
        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page

        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')

        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출 ( 114페이지 까지 있고 115페이지는 tr이 없다 )
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugon'])
    table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)
    print(table)

    for t in results:
        print(t)

def crawling_nene():
    results = []
    last = ''
    # for page in count(start=1):
    for page in range(1,5):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page

        try:
            request = Request(url)
            ssl._create_default_https_context = ssl._create_unverified_context

            response = urlopen(request)

            receive = response.read()
            html = receive.decode('utf-8', errors='replace')

            print(f'{datetime.now()}: success for request [{url}]')

        except Exception as e:
            print(f'{e} : {datetime.now()}', file=sys.stderr)
            continue

        bs = BeautifulSoup(html, 'html.parser')

        shop_infos = bs.findAll('div', attrs={'class': 'shopInfo'})
        now_shop_name = bs.find('div', attrs={'class': 'shopName'}).text


        if last == now_shop_name:
            break

        for index, shop_info in enumerate(shop_infos):
            strings = list(shop_info.strings)

            if(strings[2] != '\n'):
                shop_name = strings[6]
                shop_add = strings[8]
            else:
                shop_name = strings[4]
                shop_add = strings[6]
            if index == 0:
                last = shop_name

            results.append((shop_name, shop_add))

    # store
    table = pd.DataFrame(results, columns=['name', 'address'])

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 이 파일이 있는 dir 찾기
    RESULT_DIR = f'{BASE_DIR}/__results__'

    # table.to_csv(f'{RESULT_DIR}/nene.csv', encoding='utf-8', mode='w', index=True)  # 절대 경로 지정해주기
    table.to_csv('/root/crawling_results/nene.csv', encoding='utf-8', mode='w', index=True)
    # for t in results:
    #     print(t)


def crawling_kyochon():

    results = []

    for sido1 in range(1, 18):
            for sido2 in count(start=1):
                url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d' % (sido1, sido2)

                html = crawler.crawling(url)

                # 끝검출
                if html is None:
                    break

                bs = BeautifulSoup(html, 'html.parser')

                tag_ul = bs.find('ul', attrs={'class': 'list'})
                tag_spans = tag_ul.findAll('span', attrs={'class': 'store_item'})

                for tag_span in tag_spans:
                    strings = list(tag_span.strings)
                    name = strings[1]
                    address = strings[3].strip("\r\n\t")
                    sidogu = address.split()[:2]

                    results.append((name, address) + tuple(sidogu))


    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugon'])
    table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)
    print(table)

    for t in results:
        print(t)


def crawling_goobne():

    results = []

    url = 'http://goobne.co.kr/store/search_store.jsp'

    wd = webdriver.Chrome('D:\cafe24\chromedriver_win32\chromedriver.exe')

    wd.get(url)
    time.sleep(4)

    for page in count(start=1):
        # 자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{script}]')
        time.sleep(2)

        # 실행결과 HTML(동적으로 렌더링 된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')

        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    wd.quit()

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gugon'])
    # table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)

    for t in results:
        print(t)

if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()
    crawling_nene()
    # crawling_kyochon()
    # crawling_goobne()
