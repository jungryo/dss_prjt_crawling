# 맛집 크롤링 프로젝트
* 여러 웹사이트의 맛집을 크롤링하고 유저들의 이동경로에 있는 맛집들을 하나의 웹페이지에 보여주는 프로젝트입니다.
* 약속을 할 때 맛있는 음식을 먹고 싶지만 너무 먼 곳은 가기 싫었던 사람들이 이동하는 경로 내에 있는 맛집을 추천받으면 좋겠다는 생각으로 시작.

### Requirements
```
* Python 3.6+
* MongoDB
```
### Installation
The quick way:
```
pip install random
pip install json
pip install requests
pip install fake_useragent
pip install urllib
pip install scrapy
pip install numpy
pip install pandas
pip install matplotlib
pip install seaborn
pip install missingno
pip install geopy
pip install folium
pip install pymongo
pip install flask
```
## 프로젝트 구조도
![Alt text](https://cdn.discordapp.com/attachments/776743867772960779/786457164444074004/unknown.png)

## 필요한 작업 
1. 데이터 수집 : 5개의 웹사이트 맛집 크롤링(위도, 경도는 지도에 마커를 넣기 위해 꼭 필요) 
2. 전처리 및 DB 저장 : 수집한 데이터 전처리 후 DB에 저장
3. 이동경로의 위치 수집 : ODsay api 사용하여 이동경로의 위도, 경도 수집   
4. 프론트페이지 만들기 : flask를 사용하여 맛집데이터를 시각화 할 웹페이지 만들기
5. 프론트페이지와 DB 연결: DB와 연결하여 주소 검색시 DB에서 위,경도를 select하여 조건에 맞는 맛집 추천


> ### 1. 데이터 수집
> * 네이버, 블루리본서베이, 다이닝코드, 망고플레이트, 메뉴판 총 5개의 웹사이트에서 맛집 크롤링
> * 수집할 때 동을 기준으로 크롤링 
> * 네이버 : <https://map.naver.com/> json
> * 블루리본서베이 : <https://www.bluer.co.kr/> beautifulsoup, json
> * 다이닝코드 : <https://www.diningcode.com/> 
> * 망고플레이트 : <https://www.mangoplate.com/> json
> * 메뉴판 : <https://www.menupan.com/> scrapy
**************
* 크롤링 과정
```

```

## 전처리
```

```
## 
       
        
