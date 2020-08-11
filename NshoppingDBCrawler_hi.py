import requests
from bs4 import BeautifulSoup

catId = [50000145,50000159,50000160,50000146,50000147,50000148,50000150,50000026]

url = 'https://search.shopping.naver.com/best100v2/detail/kwd.nhn?catId={}&kwdType=KWD'

prod = []
lst = []

for i in catId:
    cateurl = url.format(str(i))
    res_url = requests.get(cateurl)
    soup = BeautifulSoup(res_url.content, 'html.parser')
    poplst = soup.find_all('a', code = 'KWD')
    for a in poplst:
        keword = a.get('title')
        if keword != None:
            prod.append({'category': i, 'product': keword})

url_shop = 'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={}&pagingSize=5&productSet=checkout&query={}&sort=rel&timestamp=&viewType=list&pagingIndex='

for w in prod:
    url_title = url_shop.format(w['product'],w['product'])
    for i in range(1,100):
        res = requests.get(url_title+str(i))
        if res.status_code == 200 :
            soup = BeautifulSoup(res.content, 'html.parser')
            f_all = soup.find_all('div', class_ = 'basicList_inner__eY_mq')
            for f in f_all:
                t_1 = f.find('a', class_ = 'basicList_link__1MaTN')     # tag of title, links and rank
                t_2 = f.find('em', class_ = 'basicList_num__1yXM9')     # tag of reviews
                title = t_1.get('title')
                link = t_1.get('href')
                reviews = str.strip(t_2.get_text())
                rank = t_1.attrs['data-nclick']
                lst.append({'category':w['category'],'product':w['product'],'title':title,'rank':rank,'reviews':reviews,'link':link})


# put shopping data in Mongo DB
from pymongo import MongoClient
client = MongoClient('mongodb://192.168.0.154:27017/')
mydb = client.mydb
makeCollection = mydb.modelingdb.insert_many(lst)
db_info = mydb.makeCollection.find()
for info in db_info:
    print(info)

client.close()