# 워드클라우드 위한 네이버 쇼핑 검색 결과 (with Request.GET)

## .format(product,product) 는 0.0.0.0/main 에서 입력받은 product 값을 반영함

import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import re
import matplotlib.pyplot as plt


url_wc = 'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={}&pagingSize=5&productSet=checkout&query={}&sort=rel&timestamp=&viewType=list&pagingIndex='.format('미숫가루','미숫가루')

board_info = []

for i in range(1,100):
    res = requests.get(url_wc+str(i))
    if res.status_code == 200 :
        soup = BeautifulSoup(res.content, 'html.parser')
        f_all = soup.find_all('div', class_ = 'basicList_inner__eY_mq')
        for f in f_all:
            t_1 = f.find('a', class_ = 'basicList_link__1MaTN')     # tag of title, links and rank
            title = t_1.get('title')
            board_info.append({'title':title})

a = []
for info in board_info: # Cursor
    a.append(info['title'])

df = pd.DataFrame({"title": a})

a = df.title.tolist() # 특정 칼럼만 리스트로 출력

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

stop_words = ['아무렇게나', '다', '게', '예컨대', '로', '나','도', '+']
# # stop_words = stop_words.split(' ')

def clean_str(text):
    pattern = '[^\w\s]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
    return text

cleaning = []
for i in range(len(a)):
    cleaning.append(clean_str(a[i]))

word_tokens = []
for i in range(len(cleaning)):
    word_tokens.append(word_tokenize(cleaning[i]))

result = [] 
for w in word_tokens: 
    if w not in stop_words: 
        result.append(w) 

# print(word_tokens) 
# print(result)

# print(word_tokens[7])
# print(result[7])

result1 = []            # 하나의 리스트화 & extend 함수(멤버 메서드) 이용하여 확장하기
for i in range(len(result)):
    result1.extend(result[i])
result1
        
import numpy as np
from wordcloud import WordCloud, STOPWORDS   # 워드클라우드 함수화
from PIL import Image

# alice_mask = np.array(Image.open("alice_mask.png")) # 워드클라우드 모형 수치화

# 폰트의 경우 경로 지정 必
def displaywordcloud (data=None, backgroundcolor='white', width=1280, height=768):
    wordcloud = WordCloud(
        font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',
        # mask = alice_mask,
        stopwords = stop_words,
        background_color = backgroundcolor,
        width = width, height = height).generate(data)
        
    plt.figure(figsize=(15,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show

# result1에 리스트로 단어가 담겨 있음
course_text = " ".join(result1)
displaywordcloud(course_text)
