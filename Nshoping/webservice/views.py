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
    driver = webdriver.Chrome('/home/sundooedu/문서/instagram/chromedriver', chrome_options=options)
    loginUrl = 'https://www.instagram.com/explore/tags/'+product_name
    driver.implicitly_wait(5)
    driver.get(loginUrl)

    # 팝업 닫기
    close_pop = driver.find_element_by_css_selector('body > div#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg > div > div > div > button')
    close_pop.click()

    # 태그 크롤링
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    popular = soup.select('div.EZdmt > div > div > div:nth-child(1)')
    
    embed=[]
    for line in popular:
        t = line.find_all('a')
        for href in t:
            embed.append(href.get('href'))
    driver.close()
    
    url1 = "https://instagram.com{}embed".format(embed[0]) 
    url2 = "https://instagram.com{}embed".format(embed[1]) 
    url3 = "https://instagram.com{}embed".format(embed[2]) 

    return render(request, 'sub.html',{'script':script, 'div':div, 'title':sub_data['title'],
                    'url1':url1, 'url2':url2, 'url3':url3})
