from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
import numpy as np
import pandas as pd
from math import pi
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from bokeh.embed import components
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import matplotlib.pyplot as plt 
from wordcloud import WordCloud, STOPWORDS   # 워드클라우드 함수화
from PIL import Image
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from tqdm import trange 
import os.path



def main(request):
    return render(request, template_name='main.html')
    
# def sub(request):
#     data = request.GET.copy()
#     return render(request,template_name='sub.html', context=data)

def sub(request):
    sub_data = request.GET.copy()
    product_name = sub_data['product']

    ### 네이버 트렌드 크롤링
    client_id = "Zxda6O8OHP58VUd07OoF"
    client_secret = "h65D3z_YOw"
    header = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret, 'Content-Type':'application/json'}
    url = "https://openapi.naver.com/v1/datalab/search"
    # body = "{\"startDate\":\"2017-01-01\",\"endDate\":\"2020-07-29\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"검색\",\"keywords\":[\"미숫가루\"]}]}" 
    body = {
    "startDate": "2017-01-01",
    "endDate": "2020-07-29",
    "timeUnit": "month",
    # "category": [{"name": "패션의류", "param": ["50000000"]}],
    "keywordGroups": [{"groupName":"검색","keywords":[product_name]}],
    }
    body = json.dumps(body, ensure_ascii=False)
    response = requests.post(url, headers = header, data = body.encode('utf-8'))
    search = json.loads(response.content)
    data4graph = search['results'][0]['data']
    df4graph = pd.DataFrame(data4graph)

    df4graph['period'] = pd.to_datetime(df4graph['period'])

    ### 보케 그래프
    p = figure(title='TEST', x_axis_type="datetime", x_axis_label='period', y_axis_label='trend ratio' , plot_height=500, plot_width=1200)
    p.xaxis.formatter = DatetimeTickFormatter(months=["%Y/%m/%d"])
    p.xaxis.major_label_orientation = pi/3
    p.line(x=df4graph.period, y=df4graph.ratio, legend_label='trend ratio', line_width=2, color='cadetblue', alpha=0.9)
    script, div = components(p)
        
    ### 인스타그램 크롤링    
    # headless options (브라우저 뜨지 않음)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")

    # URL
    # C:\Users\sundooedu\Naver-Shopping-Title-Recommendation-Service\Nshoping
    driver = webdriver.Chrome('C:/Users/sundooedu/Desktop/Nshoping/chromedriver.exe', chrome_options=options)
    loginUrl = 'https://www.instagram.com/explore/tags/'+product_name
    driver.implicitly_wait(5)
    driver.get(loginUrl)

    # 팝업 닫기
    close_pop = driver.find_element_by_css_selector('body > div#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg > div > div > div > button')
    close_pop.click()

    # 태그 크롤링
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    popular = soup.select('div.EZdmt > div > div > div:nth-of-type(1)')    #nth-child -> nth-of-type
    
    embed=[]
    for line in popular:
        t = line.find_all('a')
        for href in t:
            embed.append(href.get('href'))
    driver.close()
    
    url1 = "https://instagram.com{}embed".format(embed[0]) 
    url2 = "https://instagram.com{}embed".format(embed[1]) 
    url3 = "https://instagram.com{}embed".format(embed[2]) 


    ### 워드 클라우드
    # 워드클라우드 위한 네이버 쇼핑 검색 결과 (with Request.GET)

    ## .format(product,product) 는 0.0.0.0/main 에서 입력받은 product 값을 반영함
    url_wc = 'https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={}&pagingSize=5&productSet=checkout&query={}&sort=rel&timestamp=&viewType=list&pagingIndex='.format(product_name, product_name)
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
            
    alice_mask = np.array(Image.open("./static/alice_mask.png")) # 워드클라우드 모형 수치화
    # alice_mask = np.array(open(os.path.join('/static','alice_mask.png'), 'r'))

    # 폰트의 경우 경로 지정 必
    def displaywordcloud (data=None, backgroundcolor='white', width=1280, height=768):
        wordcloud = WordCloud(
            font_path = 'C:Windows/Fonts/NanumGothicCoding.ttf',
            mask = alice_mask,
            stopwords = stop_words,
            background_color = backgroundcolor,
            width = width, height = height).generate(data)
        fig = plt.figure(figsize=(15,10))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        # plt.show
        # fig.savefig('./static/wordcloud.png')
        
    # result1에 리스트로 단어가 담겨 있음
    course_text = " ".join(result1)
    displaywordcloud(course_text)


    return render(request, 'sub.html',{'script':script, 'div':div, 'title':sub_data['title'],
                    'url1':url1, 'url2':url2, 'url3':url3})
