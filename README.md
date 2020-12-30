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

https://github.com/kim-so-hyeon/Naver-Shopping-Title-Recommendation-Service/edit/develop/README.md
