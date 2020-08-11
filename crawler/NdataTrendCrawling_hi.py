import json
import pandas as pd
import requests
import time
client_id = "Zxda6O8OHP58VUd07OoF"
client_secret = "h65D3z_YOw"
header = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret, 'Content-Type':'application/json'}
url = "https://openapi.naver.com/v1/datalab/search"

def Ntrend(request):
    product = request.GET['product']
    today = time.strftime("%Y-%m-%d")
    body = "{\"startDate\":\"2017-01-01\",\"endDate\":\"{}\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"검색\",\"keywords\":\"{}\"}]}".format(today,product)
    response = requests.post(url, headers = header, data = body.encode('utf-8'))    # 네이버 검색 트렌드는 post 방식으로 요청됨
    search = json.loads(response.content)   # dictionary 형태임
    data4graph = search['results'][0]['data']   # data4graph는 list 속의 딕셔너리로 구성됨 / search의 키는 (['startDate', 'endDate', 'timeUnit', 'results'])
    df4graph = pd.DataFrame(data4graph)   # 그래프를 그리기 위한 Dataframe으로 변환
    return df4graph