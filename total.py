import sqlite3
import pandas as pd
import numpy as np
import re
from tqdm import trange
from pymongo import MongoClient

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

import matplotlib.pyplot as plt

client = MongoClient('mongodb://192.168.0.154:27017/')  # mongo 연결
mydb = client.mydb
board_info = mydb.modelingdb # get Collection with find()

data_df = pd.DataFrame(list(board_info.find()))

def clean_str(text):
    pattern = '[-=,#/\?:^$.@\"※~&ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl=' ', string=text)
    return text

# map 함수 : Series에서 사용하며 모든 요소에 함수 일괄 적용
# apply 함수 : DataFrame에서 사용하며 각각의 행 또는 열(Series)에 함수 일괄 적용
# applymap 함수 : DataFrame에서 사용하며 모든 요소에 함수 일괄 적용

data_df['title'] = data_df.title.map(clean_str) # 특수기호 제거

# category, product, title → total열로 통합
data_df['category'] = data_df['category'].astype(str)
data_df['total'] = data_df['category']+' '+data_df['product']+' '+data_df['title']
data_df = data_df[['category','product','title','total','rank']]

# # data_df['total'] = data_df.total.map(word_tokenize)
data_df['total'] = data_df['total'].str.replace("    "," ")
data_df['total'] = data_df['total'].str.replace("   "," ")
data_df['total'] = data_df['total'].str.replace("  "," ")
data_df['total2'] = data_df['total'].str.split(" ")

data_df = data_df[['category','product','title','total','total2','rank']]

result = []                 # 하나의 리스트화 & extend 함수(멤버 메서드) 이용하여 확장하기
for i in trange(len(data_df.title)):
    result.append(word_tokenize(data_df.title[i]))

data_df['title'] = result
data_df['title']

splitlst = (data_df['rank'].str.split(',',2))

ranking = []

for i in splitlst:
     ranking.append((i[2].split(':',1)[1]))

data_df['rank'] = ranking
data_df['rank']

# db에서 rank값이 text(str)으로 되어있었으므로, 계산위해 int 형으로 변경

data_df['rank'] = data_df['rank'].astype('int32')
rank_max = data_df.groupby(['product'])['rank'].max().reset_index(drop = False)

# 상품명으로 그룹핑하여 최대 랭크값을 찾아 해당 행의 랭크 위치값 도출
score = []

for i in trange(len(data_df)):
    p = data_df['product'][i]
    r = data_df['rank'][i]
    for w in range(len(rank_max)):
        if p == rank_max['product'][w]:
            a = r / rank_max['rank'][w]
            score.append(a)

# 랭크 위치값을 4가지 그룹으로 나누기

s_result = []

for i in score:
    if i >= 0.75:
        s_result.append('D')
    else:
        if i >= 0.5:
            s_result.append('C')
        else:
            if i >= 0.25:
                s_result.append('B')
            else:
                s_result.append('A')

data_df['score'] = s_result

data_df['rank'] = data_df['rank'].astype('str')

mongo = []

for i in range(len(data_df)):
    cate = data_df['category'][i]    
    prod = data_df['product'][i]
    title = data_df['title'][i]
    total = data_df['total'][i]
    total2 = data_df['total2'][i]
    score = data_df['score'][i]
    rank = data_df['rank'][i]
    mg_dict = {'category':cate, 'product':prod, 'title':title,'total':total,'total2':total2,'rank':rank,'score':score}
    mongo.append(mg_dict)

mongo

print(mongo)

# from pymongo import MongoClient
# client = MongoClient('mongodb://192.168.0.154:27017/')
# mydb = client.mydb
# makeCollection = mydb.processed.insert_many(mongo)

client.close()