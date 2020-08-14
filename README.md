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


### [instagram 인기 게시물 크롤링](https://github.com/kim-so-hyeon/Naum-Web-Service/blob/master/webservice/views.py)

![스크린샷, 2020-08-14 15-52-51](https://user-images.githubusercontent.com/64175895/90222167-7e85db00-de46-11ea-9989-deae1b250b69.png)

### [텍스트 특수기호 클렌징 작업](https://github.com/kim-so-hyeon/Naver-Shopping-Title-Recommendation-Service/blob/develop/MakeResultVal_hi.ipynb)

원하는 장소를 검색하여 추가하고, 관련 날씨 정보를 볼 수 있다

![](./images/display-6.gif)

### [워드클라우드 함수화](https://github.com/kim-so-hyeon/Naver-Shopping-Title-Recommendation-Service/blob/develop/Naver%20shopping%20preprocessing.ipynb)

온도 단위를 **섭씨 혹은 화씨**로 변환하여 볼 수 있다

![](./images/display-7.gif)

### 사용자 설정 저장

다음 설정을 저장하여 앱을 다시 실행시, 기존의 설정대로 실행되도록 한다

| 추가한 장소                 | 온도 단위 설정              | 마지막으로 본 페이지         |
| --------------------------- | --------------------------- | ---------------------------- |
|                             |                             |                              |
| --------------------------- | --------------------------- | ---------------------------- |
| ![](./images/display-8.gif) | ![](./images/display-9.gif) | ![](./images/display-10.gif) |

&nbsp;

---

## 모델 설계 및 구현

### View Controller 구성

![](./images/implementation-1.jpeg)

&nbsp;

### 날씨 모델과 View - MVVM

#### WeatherViewController - WeatherViewModel

![](./images/implementation-2.jpeg)

- ViewModel 의 view 관련 type 에 Observer 를 등록할 수 있는 타입을 구현
  - `Observable` protocol
  - ViewModel - CurrentWeather, HourlyWeatherItem, DailyWetherItem, DetailWeather 대상 data 변화에 대해 observer 를 등록할 수 있다
  - observer handler 에 관련 view 나 label text 를 변경할 수 있는 함수를 등록
  - view model 변경시에 해당 observer가 실행되어 view 도 같이 그에 맞게 업데이트 된다

&nbsp;

### 역할 분배

#### view 관련

| class / struct               | 역할                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `PageViewController`         | LocationManager 사용해서 받은 현재위치를 포함하여, 저장된 위치의 날씨를 보여줄 WeatherViewController 를 보여준다 |
| `WeatherViewController`      | Location 객체에 해당하는 위치 정보를 보여준다                |
| `WeatherViewModel`           | - OpenWeatherMapService 를 이용하여 위치에 맞는 날씨 정보를 가져온다<br />- WeatherBuilder 객체를 통해 가져온 정보를 view 에 필요한 데이터 타입들로 만든다 |
| `WeatherBuilder`             | 네트워킹을 통해 받아온 `WeatherData` 객체를 view model 의 각 필요에 맞게 가공한다 |
| `LocationListViewController` | - 저장된 위치를 사용자에게 보여준다 <br />- 저장된 위치를 삭제한다 <br />- 온도 단위를 바꾼다 <br />- SearchViewController 를 보여준다 |
| `SearchViewController`       | - 사용자 검색 문자열을 사용하여 위치 자동완성 <br />- 사용자가 선택한 위치 정보(장소이름, 위도, 경도) 를 LocationViewController delegate 통해 넘긴다 |
| `Observable`                 | - ViewModel 의 각 데이터 타입에 observer 기능을 구현하기 위한 generic type<br />- `WeatherViewModel` 에서 observer 등록이 필요한 속성에 사용됨 |



#### Utilities

| class / struct          | 역할                                                         |
| ----------------------- | ------------------------------------------------------------ |
| `LocationManager`       | CLLocationManager 사용하여 현재 위치 가져오기                |
| `OpenWeatherMapService` | - 네트워킹 통한 날씨 예측 정보 가져오기<br />- `WeatherData` 타입으로 json decoding 하기 |
| `WeatherBuilder`        | `WeatherData` → `WeatherViewModel` 이 가진 각 type으로 데이터 가공 |
| `WindDirection`         | 바람의 방향 값(360도 내)을 compass direction으로 변환        |
| `DateConverter`         | 주어진 timezone 을 사용하여 문자열로 된 날짜를 변환해 주는 역할 |

&nbsp;

### Weather Model Hierarchy

![](./images/weather-hierarchy.png)

&nbsp;

### ViewController 간 Data 주고 받기 - Delegate 사용

[*관련 학습한 내용- 1*](#view-controller-양방향-데이터-전달)     [*관련 학습한 내용- 2*](https://daheenallwhite.github.io/ios/2019/07/22/Delegation/)

view controller 간 데이터를 backward 로 받기 위해서, delegate protocol 을 구현하여 사용

![](./images/implementation-delegate.jpg)



&nbsp;

### 현재 위치 - CLLocationManager 활용

> `LocationMagnager` class 로 구현

#### 위치 가져오는 과정

1. `CLLocationManager` 객체 생성
2. location 데이터의 정확도 설정 : `desiredAccuracy` property 설정
3. 사용자에게 위치정보 사용 허가 받기 : `requestWhenInUseAuthorization()` method 
4. 위치 요청이 가능한 허가 상태 `CLAuthorizationStatus` : `.authorizedWhenInUse` / `.authorizedAlways`
5. 위치 요청: `requestLocation()`
   - 해당 method는 즉각 return 한다
   - 위치 값을 얻은 후, delegate 의 `didUpdateLocation` method 를 호출한다
6. Delegate method - `didUpdateLocation` 

&nbsp;

### 날씨 정보 받아오기 & 파싱하기 - OpenWeather API / URLSession / Codable

>  [5 days / 3 hours forecast api](https://openweathermap.org/forecast5)

*API JSON 구조 (orange color : 배열 구조)*

![](./images/api-data-structure.png)

- [URLSession 학습한 내용](#url-loading-system)
- Codable : `Data` → `WeatherData` 변환하기
  - `WeatherData` 는 `Codable` protocol 을 준수
  - `JSONDecoder` 사용하여 변환

&nbsp;

### 장소 검색 & 자동완성 - MKLocalSearchCompleter 

> 문자열로 위치를 제공하면 그에 맞는 자동완성된 comletion string list 를 제공하는 utility 객체

- 구현 원리 

  ![](./images/implementation-search.jpeg)

- `results` property : `MKLocalSearchCompleter` 의 자동완성 처리된 데이터를 얻는 속성
  - `MKLocalSearchCompletion` type
  - 직접 생성할 수는 없다. Completer 에 의해서만 생성되는 객체
- completion 될 대상 지정 방법
  - 위치 문자열, 지역, 필터 타입 등을 지정할 수 있다.
  - 도시명 검색 : `queryFragment` property 에 사용자가 입력하는 문자열 설정
  - 필터 타입 : locationAndQueries / locationsOnly 
- delgate : search completion data 를 가져오기 위한 메소드가 정의됨
  - `MKLocalSearchCompleterDelegate`
  - `completerDidUpdateResults()` 메소드 : completer 가 검색 완성 배열을 업데이트 한 뒤 호출하는 메소드.
  - 이 메소드 안에 search 결과 table view 를 reload 하도록 구현함

&nbsp;

### 사용자 설정 저장 - UserDefaults

[*관련 학습한 내용*]()

사용자 설정 항목

- 마지막으로 본 날씨의 위치 
- 사용자가 저장한 위치 리스트
- 온도 단위 선택 정보

UserDefaults 에 사용될 key 관리하는 struct `DataKeys`

&nbsp;

### API 데이터 기반 시간 구하기

API 에서 받아온 date & time (UTC 표준)  → 각 나라별 시간으로 변환하기

1. `list.dt_text` string (utc 단위 시간) → `Date` 객체로 변환
2. `city.timezone` : 해당 도시의 시간을 UTC로부터 변환하기 위한 차이값. 단위는 초
3. 각 도시의 시간 = `list.dt_txt` 를 date로 변환한 객체 + `city.timezone`
4. 차이값 더해주기 : `Date` - `addingTimeInterval()` method 사용

&nbsp;

### 온도 단위 설정대로 정보 보여주기 - Singleton 활용

- Singleton 으로 구현한 이유
  - view controller 뿐만 아니라 날씨 관련된 거의 모든 data model 에서 온도와 관련된 부분이 많음
  - Singleton 통해서 하나의 인스턴스로 사용자가 설정한 온도 단위를 이용하는게 적절하다고 판단

- `TemperatureUnit` 의 `shared` property 로 단위 접근 가능

&nbsp;

---

# What is Naum Service ?

![image](https://newsimg.hankookilbo.com/cms/articlerelease/2020/08/08/4c8c98e2-84b1-4426-bf07-4a534605bc4e.png)</br>
[이미지 출처:https://www.hankookilbo.com/News/Read/A2020080801130005439?did=NA]
</br>
- 플랫폼 기업의 다양한 창업 지원책으로 중장년층의 온라인 창업이 늘어나고 있습니다. 특히 네이버 스마트스토어는 소상공인을 위한 쉽고 다양한 기술 지원과 교육을 병행하고 있어 판매자 수와 매출액의 꾸준한 증가를 보여주고 있습니다.
국내 온라인 창업이나 부업으로 네이버 스마트스토어의 선택이 높아짐에 따라 데이터를 활용하여 온라인 판매 초심자에게 상품명에 대한 가이드를 제공하고자 하는 것이 NAUM Project의 시작입니다.

&nbsp;

## Naum 서비스 메인 페이지 화면
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f33d3e1b81df3575cfbc6d9/1c63d7acf3df27af522029da1bf9b667/MainPage.png)

- 네이버 쇼핑에서 식품분야만을 서비스 대상으로 우선 선정하였습니다.
메인화면에서 네이버와 동일하게 카테고리를 설정하게 하였고, 상품명과 제목을 각각 입력할 수 있도록 입력창을 생성하였습니다. 

&nbsp;

## 로딩 페이지 추가
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f33d3e1b81df3575cfbc6d9/f139ccb65e31d77ac8e2666d5e314562/LoadingPage.png)

- 서비스 제공을 위해 로딩시간이 발생되어, input값이 들어올 경우 로딩시간 동안 노출되는 로딩페이지를 추가하였습니다. 

&nbsp;

## 서비스 화면 Example 1
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f33d3e1b81df3575cfbc6d9/f20b729646cca32cc1c232287315f4f0/image.png)
- 랭킹 순위를 기준으로 등급을 4가지(A,B,C,D)로 나누었습니다. 
- 랭킹이 높은 등급 A의 테스트 데이터로 Naum검색을 해 본 화면입니다. 
- 제목에 대한 등급뿐만 아니라 상품 마케팅을 위한 서비스를 추가적으로 제공하였습니다.
  - ① 네이버스토어에서 해당 상품명과 같이 가장 많이 쓰인 키워드들 제공
  - ② 상품명의 최근 3년간 네이버 검색어 트렌드를 Bokeh를 이용한 그래프로 시각화하여 제공
  - ③ instagram에서 해당 상품명을 해시태그로 검색하였을 때 인기게시물로 상위에 노출되는 피드 제공

&nbsp;

## 서비스 화면 Example 2
![image](https://trello-attachments.s3.amazonaws.com/5ef9b25e65d7ed813a5ae0ce/5f33d3e1b81df3575cfbc6d9/8a8379fd896c6b2fb89511b0ee13bb06/image.png)

&nbsp;
