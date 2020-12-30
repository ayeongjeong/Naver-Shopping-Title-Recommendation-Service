# NAUM 서비스 프로젝트(Naver-shopping Attractive User Message)  
>	**[네이버 스마트스토어 상품의 카테고리·종류·제목에 관한 등급 테스트 서비스 바로 이동하기](https://naum-test-frcsq.run.goorm.io/main/)**  

&nbsp;

## 프로젝트 주제 선정 이유와 목표
- 스마트 스토어를 부업으로 하는 직장인들이 늘고 있는 추세이며, 해당 경우 상품명이 가장 먼저 고객에게 비춰지는 중요한 요소인데 처음 스토어를 진입할때에 어려움이 있다고 판단

- 소상 공인/스마트스토어를 부업으로 운영하는 직장인/네이버 쇼핑 초심자에게 데이터를 통해 소비자를 설득할 수 있는 상품명 가이드 제시

&nbsp;

## 프로젝트 진행 과정

- [전처리](#전처리-과정)
- [모델 설계 및 구현](#모델-설계-및-구현)
- [WEB Server 구동 화면](#WEB-Server-구동-화면)

&nbsp;

### 구성원 및 역할 분담

| 구성원 이름          | 역할                                                         |
| ----------------------- | ------------------------------------------------------------ |
|       `김소현`        | `텍스트 데이터 전처리` & `DB생성 및 구축` & `워드클라우드 작업`              |
|       `윤혜인`        | `네이버 검색어 및 트렌드 크롤링` & `데이터 EDA 및 모델링`&`최종 보고서 작성` |
|       `정아영`        | `Django 웹 서버 구축 및 디자인` & `시각화, 인스타그램 크롤링 작업` & `모델 선정 및 테스트`  |

&nbsp;

---
## 전처리 과정

- [상품 관련 검색어 트렌드 크롤링](#상품-관련-검색어-트렌드-크롤링)
- [instagram 인기 게시물 크롤링](#instagram-인기-게시물-크롤링)
- [텍스트 특수기호 클렌징 작업](#텍스트-특수기호-클렌징-작업)
- [워드클라우드 함수화](#워드클라우드-함수화)

 &nbsp;

### [상품 관련 검색어 크롤링](https://github.com/kim-so-hyeon/Naver-Shopping-Title-Recommendation-Service/blob/develop/NshoppingDBCrawler_hi.py)

![스크린샷, 2020-08-14 15-50-55](https://user-images.githubusercontent.com/64175895/90222165-7b8aea80-de46-11ea-89a0-9286b278c23e.png)
Requests, BeautifulSoup 크롤링 / Background_tasks 스케쥴링 → 모델링 학습 데이터 및 WordCloud

### [instagram 인기 게시물 크롤링](https://github.com/kim-so-hyeon/Naum-Web-Service/blob/master/webservice/views.py)

![스크린샷, 2020-08-14 15-52-51](https://user-images.githubusercontent.com/64175895/90222167-7e85db00-de46-11ea-9989-deae1b250b69.png)
Selenium 크롤링 → 실시간 이미지 수집

### [텍스트 특수기호 클렌징 작업](https://github.com/kim-so-hyeon/Naver-Shopping-Title-Recommendation-Service/blob/develop/MakeResultVal_hi.ipynb)

![스크린샷, 2020-08-14 16-23-31](https://user-images.githubusercontent.com/64175895/90224385-88a9d880-de4a-11ea-9cc6-7e8501f4b23e.png)

### [워드클라우드 함수화](https://github.com/kim-so-hyeon/Naver-Shopping-Title-Recommendation-Service/blob/develop/Naver%20shopping%20preprocessing.ipynb)

![스크린샷, 2020-08-14 16-25-14](https://user-images.githubusercontent.com/64175895/90224535-c60e6600-de4a-11ea-88d6-332f8e4d0286.png)

&nbsp;

---

## 모델 설계 및 구현

### 모델 선정
1. LSTM
- 네이버 쇼핑에 검색된 상품 제목으로, 등록하려는 상품의 쇼핑검색 상위 노출 여부를 예측할 수 있을 것이다. 일반적으로 네이버 스마트 스토어 / 윈도에 상품을 등록할 때, 네이버 쇼핑검색 상위에 노출되는 상품을 참고하여 등록
2. CNN - Convolution1D
- 네이버 쇼핑에 검색된 상품 제목으로, 등록하려는 상품의 쇼핑검색 상위 노출 여부를 예측할 수 있을 것이다. 일반적으로 네이버 스마트 스토어 / 윈도에 상품을 등록할 때, 네이버 쇼핑검색 상위에 노출되는 상품을 참고하여 등록

&nbsp;

### 모델 평가 

![스크린샷, 2020-08-14 16-32-59](https://user-images.githubusercontent.com/64175895/90225203-e1c63c00-de4b-11ea-9e4b-9f68c92301c1.png)

CNN 모델의 한계점
1. 과적합 : traon 데이터는 loss가 줄어드는 모습을 보이지만, test 데이터는 loss 상승
2. Precision이 낮음

&nbsp;

### 모델을 이용한 서비스 구조

![스크린샷, 2020-08-14 16-36-25](https://user-images.githubusercontent.com/64175895/90225432-54371c00-de4c-11ea-8886-ad480c20a239.png)

&nbsp;

---
# WEB Server 구동 화면

# What is Naum Service ?

![image](https://newsimg.hankookilbo.com/cms/articlerelease/2020/08/08/4c8c98e2-84b1-4426-bf07-4a534605bc4e.png)</br>
[이미지 출처:https://www.hankookilbo.com/News/Read/A2020080801130005439?did=NA]
</br>
- 플랫폼 기업의 다양한 창업 지원책으로 중장년층의 온라인 창업이 늘어나고 있습니다. 특히 네이버 스마트스토어는 소상공인을 위한 쉽고 다양한 기술 지원과 교육을 병행하고 있어 판매자 수와 매출액의 꾸준한 증가를 보여주고 있습니다.
국내 온라인 창업이나 부업으로 네이버 스마트스토어의 선택이 높아짐에 따라 데이터를 활용하여 온라인 판매 초심자에게 상품명에 대한 가이드를 제공하고자 하는 것이 NAUM Project의 시작입니다.

&nbsp;

## Naum 서비스 메인 페이지 화면
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f5ad939307f625dbbb2d348/3da8814bf7eacab2d09d70d173da8df7/main.PNG)

- 네이버 쇼핑에서 식품분야만을 서비스 대상으로 우선 선정하였습니다.
메인화면에서 네이버와 동일하게 카테고리를 설정하게 하였고, 상품명과 제목을 각각 입력할 수 있도록 입력창을 생성하였습니다. 

&nbsp;

## 메인 페이지 하단 프로젝트 팀 정보 추가
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f5ad939307f625dbbb2d348/7d6d4f572f6bee75a73f5bd026a95fd9/team.PNG)
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f5ad939307f625dbbb2d348/6680b5aa0cc1e91fec09bd51357859ea/contact.PNG)

- 메인 페이지 하단에 팀소개 부분과 팀과 연락할 수 있는 Contact Us 부분을 추가하였습니다. 

&nbsp;

## 로딩 페이지 추가
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f33d3e1b81df3575cfbc6d9/f139ccb65e31d77ac8e2666d5e314562/LoadingPage.png)

- 서비스 제공을 위해 로딩시간이 발생되어, input값이 들어올 경우 로딩시간 동안 노출되는 로딩페이지를 추가하였습니다. 

&nbsp;

## 서비스 페이지 Example
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f5ad939307f625dbbb2d348/1e215899d473b110f436a75b0d76acf9/grade.PNG)
![image](https://trello-attachments.s3.amazonaws.com/5f5ad939307f625dbbb2d348/944x612/64ad0509365b840fbca763e832dd8b7b/wordcloud.PNG.png)
![image](https://trello-attachments.s3.amazonaws.com/5f5ad939307f625dbbb2d348/1065x697/8c7c9d16bac7cdb8f6bac91ba25d0581/trend.PNG.png)
![image](https://trello-attachments.s3.amazonaws.com/5f5ad939307f625dbbb2d348/1090x771/92e5c374cd4da2101d26b6590a0effd2/instagram.PNG.png)
- 랭킹 순위를 기준으로 등급을 4가지(A,B,C,D)로 나누었습니다. 
- A등급의 결과가 나온 Naum 서비스 화면입니다. 
- 제목에 대한 등급뿐만 아니라 상품 마케팅을 위한 서비스를 추가적으로 제공하였습니다.
  - ① 네이버스토어에서 해당 상품명과 같이 가장 많이 쓰인 키워드들 제공
  - ② 상품명의 최근 3년간 네이버 검색어 트렌드를 Bokeh를 이용한 그래프로 시각화하여 제공
  - ③ instagram에서 해당 상품명을 해시태그로 검색하였을 때 인기게시물로 상위에 노출되는 피드 제공

&nbsp;
