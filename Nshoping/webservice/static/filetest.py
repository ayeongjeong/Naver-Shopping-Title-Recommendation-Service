# from PIL import Image
import numpy as np
import urllib.request
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS   # 워드클라우드 함수화
from PIL import Image
import nltk
# nltk.download('punkt')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
# from tqdm import trange 
# import os.path
import requests
import pandas as pd


### 워드 클라우드
    # 워드클라우드 위한 네이버 쇼핑 검색 결과 (with Request.GET)
product_name = '미숫가루'
    ## .format(product,product) 는 0.0.0.0/main 에서 입력받은 product 값을 반영함
url_wc = 'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={}&pagingSize=5&productSet=checkout&query={}&sort=rel&timestamp=&viewType=list&pagingIndex='.format(product_name, product_name)
board_info = []

for i in range(1,2):
    res = requests.get(url_wc+str(i))
    if res.status_code == 200 :
        soup = BeautifulSoup(res.content, 'html.parser')
        f_all = soup.find_all('div', class_ = 'basicList_inner__eY_mq')
        for f in f_all:
            t_1 = f.find('a', class_ = 'basicList_link__1MaTN')     # tag of title, links and rank
            title = t_1.get('title')
            board_info.append({'title':title})
# print(board_info)

a = []
for info in board_info: # Cursor
    a.append(info['title'])

df = pd.DataFrame({"title": a})
a = df.title.tolist()

# nltk.download('punkt')

stop_words = ['아무렇게나', '다', '게', '예컨대', '로', '나','도', '+']
# # stop_words = stop_words.split(' ')

word_tokens = []
for i in range(len(a)): #trange
    word_tokens.append(word_tokenize(a[i]))

result = [] 
for w in word_tokens: 
    if w not in stop_words: 
        result.append(w) 

result1 = []            # 하나의 리스트화 & extend 함수(멤버 메서드) 이용하여 확장하기
for i in range(len(result)):    #trange
    result1.extend(result[i])
result1
        

# alice_mask = np.array(Image.open("../webservice/static/alice_mask.png")) # 워드클라우드 모형 수치화
# alice_mask = np.array(open(os.path.join('/static','alice_mask.png'), 'r'))

# 폰트의 경우 경로 지정 必
def displaywordcloud (data=None, backgroundcolor='white', width=800, height=700):
    wordcloud = WordCloud(
        # font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',
        font_path = 'C:Windows/Fonts/NanumGothicCoding.ttf',
        # mask = alice_mask,
        stopwords = stop_words,
        background_color = backgroundcolor,
        width = width, height = height).generate(data)
    fig = plt.figure(figsize=(15,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show
    print("된다!!!!!")
    # fig.savefig('./static/wordcloud.png')
    # fig.save_file('./static/wordcloud.png')

    
# result1에 리스트로 단어가 담겨 있음
course_text = " ".join(result1)
displaywordcloud(course_text)