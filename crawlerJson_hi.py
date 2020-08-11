# JavaScript로 더보기 기능이 되어있어서, 페이지당 40개씩 노출되도록 해둬도 5개가 첫 페이지에 노출돼서 기존에는 5개씩 100페이지 돌리도록 했음
# 페이지 소스에서 하단에 더보기가 불러오는 데이터가 전부 들어있음 (json 형식)
import requests
from bs4 import BeautifulSoup
import json

url_wc = 'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={}&pagingSize=100&productSet=checkout&query={}&sort=rel&timestamp=&viewType=list&pagingIndex='.format('미숫가루', '미숫가루')
board_info = []

res = requests.get(url_wc)
if res.status_code == 200 :
    soup = BeautifulSoup(res.content, 'html.parser')
    f_all = soup.find_all('script', id = '__NEXT_DATA__')
    f_txt = str.strip(f_all[0].get_text())      # string 형태로 넣어진 데이터
    json_data = json.loads(f_txt)       # json으로 로드
    json_string = json_data["props"]["pageProps"]["initialState"]["products"]["list"]       # nth level 로 접근해서 요소 가져오기
    
a = []

for dic in json_string:     # 상품 하나마다 item 이라는 key 로 묶여있음
    content = dic['item']
    title = content['productTitle']
    a.append(title)
a

## 원래 사용했던 코드 : for 문이 길어서 로딩 시간이 오래걸림
# board_info = []

# for i in range(1,100):
#     res = requests.get(url_wc+str(i))
#     if res.status_code == 200 :
#         soup = BeautifulSoup(res.content, 'html.parser')
#         f_all = soup.find_all('div', class_ = 'basicList_inner__eY_mq')
#         for f in f_all:
#             t_1 = f.find('a', class_ = 'basicList_link__1MaTN')     # tag of title, links and rank
#             title = t_1.get('title')
#             board_info.append({'title':title})

# a = []
# for info in board_info: # Cursor
#     a.append(info['title'])