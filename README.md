# 맛집 크롤링 프로젝트
* 여러 웹사이트의 맛집을 크롤링하고 유저들의 이동경로에 있는 맛집들을 하나의 웹페이지에 보여주는 프로젝트입니다.
## 프로젝트 계기
* 약속을 할 때 맛있는 음식을 먹고 싶지만 너무 먼 곳은 가기 싫었던 사람들이 이동하는 경로 내에 있는 맛집을 추천받으면 좋겠다는 생각으로 시작.
## Requirements
```
* Python 3.6+
```
## Installation
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
```
## 데이터 수집
* 네이버, 블루리본서베이, 다이닝코드, 망고플레이트, 메뉴판 총 5개의 웹사이트에서 맛집 크롤링
* 수집할 때 동을 기준으로 크롤링 
* 네이버 : <https://map.naver.com/>
* 블루리본서베이 : <https://www.bluer.co.kr/>
* 다이닝코드 : <https://www.diningcode.com/>
* 망고플레이트 : <https://www.mangoplate.com/>
* 메뉴판 : <https://www.menupan.com/>
**************
1. 네이버 
```
import random
import time
import pandas as pd
import requests
from scrapy.http import TextResponse
from fake_useragent import UserAgent
import warnings

idx = 0
errorlist = []
ua = UserAgent()
columns = ["id", "dong", "name", "tel", "addr", "bizhour", "category", "context", "menu", "reviewcount", "microreview", "thumbnail", "lng", "lat", "rating"]
df = pd.DataFrame(columns=columns)

for i in range(0, len(dongs["동"]), 50):
    for dong in dongs["동"][i:i+50]:
        # 크롤링 URL 설정
        url = "https://map.naver.com/v5/api/search?caller=pcweb&query={} 맛집&type=all&searchCoord=126.93536503149417;37.576196000000024&page=1&displayCount=50&isPlaceRecommendationReplace=true&lang=ko".format(dong)

        # 네이버 지도 (URL+동 이름)으로 해당 지역 맛집 데이터 리퀘스트
        try:
            response = requests.get(url)
            print(idx, dong, response)
            datas = response.json()["result"]["place"]["list"]
        except:
            errorlist.append(idx)
        
        # 해당 동 데이터 입력
        columns = ["id", "dong", "name", "tel", "addr", "bizhour", "category", "context", "menu", "reviewcount", "microreview", "thumbnail", "lng", "lat", "rating"]
        dong_df = pd.DataFrame(columns=columns)
        
        try :
            dong_df["dong"] = dong
            dong_df["id"] = [data["id"] for data in datas]
            dong_df["name"] = [data["name"] for data in datas]
            dong_df["tel"] = [data["tel"] for data in datas]
            dong_df["addr"] = [data["address"] for data in datas]
            dong_df["bizhour"] = [data["bizhourInfo"] for data in datas]
            dong_df["category"] = [data["category"] for data in datas]
            dong_df["context"] = [data["context"] for data in datas]
            dong_df["menu"] = [data["menuInfo"] for data in datas]
            dong_df["reviewcount"] = [data["reviewCount"] for data in datas]
            dong_df["microreview"] = [data["microReview"] for data in datas]
            dong_df["thumbnail"] = [data["thumUrl"] for data in datas]
            dong_df["lng"] = [data["x"] for data in datas]
            dong_df["lat"] = [data["y"] for data in datas]
        
        except:
            print("none data", idx, dong)
    
        idx += 1
        df = df.append(dong_df)
        time.sleep(random.randint(15, 20))
    
    time.sleep(random.randint(180, 240))
```

