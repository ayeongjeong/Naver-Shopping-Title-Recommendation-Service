
import requests
from bs4 import BeautifulSoup
import sqlite3

# # Create table
# conn = sqlite3.connect('db.sqlite3')
# query = 'CREATE TABLE navershop (title TEXT, reviews TEXT, rank TEXT, link TEXT)'
# conn.execute(query)
# conn.commit()
# conn.close()

from background_task import background
import time

url = 'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery=%EB%AF%B8%EC%88%AB%EA%B0%80%EB%A3%A8&pagingSize=5&productSet=checkout&query=%EB%AF%B8%EC%88%AB%EA%B0%80%EB%A3%A8&sort=rel&timestamp=&viewType=list&pagingIndex='

@background
def task_crawling_naver(schedule = 60, repeat = 60*30):
    for i in range(1,100):
        res = requests.get(url+str(i))
        if res.status_code == 200 :
            soup = BeautifulSoup(res.content, 'html.parser')
            f_all = soup.find_all('div', class_ = 'basicList_inner__eY_mq')
            with sqlite3.connect('db.sqlite3') as con:
                cur = con.cursor()
                title = ''
                link = ''
                reviews = ''
                rank = ''
                for f in f_all:
                    t_1 = f.find('a', class_ = 'basicList_link__1MaTN')     # tag of title, links and rank
                    t_2 = f.find('em', class_ = 'basicList_num__1yXM9')     # tag of reviews
                    title = t_1.get('title')
                    link = t_1.get('href')
                    reviews = str.strip(t_2.get_text())
                    rank = t_1.attrs['data-nclick']
                    cur.execute('INSERT INTO navershop (title, reviews, rank, link) VALUES (?,?,?,?)', (title, reviews, rank, link))
                con.commit()
        time_tuple = time.localtime()
        time_str = time.strftime('%m/%d/%Y, %H:%M:%S', time_tuple)
    print('crawling_naver_shopping :', time_str)

