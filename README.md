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
pip install BeautifulSoup4
pip install selenium
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
# 프로젝트 구조도
![Alt text](https://cdn.discordapp.com/attachments/776743867772960779/786457164444074004/unknown.png)

# 필요한 작업 
1. 데이터 수집 : 5개의 웹사이트 맛집 크롤링(위도, 경도는 지도에 마커를 넣기 위해 꼭 필요) 
2. 전처리 및 DB 저장 : 수집한 데이터 전처리 후 DB에 저장
3. 이동경로의 위치 수집 : ODsay api 사용하여 이동경로의 위도, 경도 수집   
4. 프론트페이지 만들기 : flask를 사용하여 맛집데이터를 시각화 할 웹페이지 만들기
5. 프론트페이지와 DB 연결: DB와 연결하여 주소 검색시 DB에서 위,경도를 select하여 조건에 맞는 맛집 추천   
   
> ### 1. 데이터 수집
> * 네이버, 블루리본서베이, 다이닝코드, 망고플레이트, 메뉴판 총 5개의 웹사이트에서 맛집 크롤링
> * 네이버 : <https://map.naver.com/> (json 사용)
> * 블루리본서베이 : <https://www.bluer.co.kr/> (BeautifulSoup, json 사용)
> * 다이닝코드 : <https://www.diningcode.com/> (selenium 사용)
> * 망고플레이트 : <https://www.mangoplate.com/> (json 사용)
> * 메뉴판 : <https://www.menupan.com/> scrapy (scrapy 사용)
**********
**scrapy spider.py**
```
import scrapy
import re
from menupan.items import MenupanItem

class MenupanSpider(scrapy.Spider):
    name = "Menupan"
    start_urls = ["http://www.menupan.com/restaurant/bestrest/bestrest.asp?page={}&pt=wk".format(i) for i in range(1, 41)]
    
    def parse(self, response):
        links = response.xpath('/html/body/div/div[1]/div[1]/div[4]/div[4]/ul/li/p[1]/a/@href').extract()
        links = list(map(response.urljoin, links))
        for link in links:
            yield scrapy.Request(link, callback=self.page_parse)
            
    def page_parse(self, response):
        item = MenupanItem()
        item["name"] = response.xpath('/html/body/center/div[2]/div[2]/*[@class="areaBasic"]/*[@class="restName"]/*[@class="name"]/text()').extract()[0].replace("\xa0", "")
        item["tel"] = response.xpath('/html/body/center/div[2]/div[2]/*[@class="areaBasic"]/*[@class="restTel"]/*[@class="tel1"]/text()').extract()[0].replace("(", "").replace(")", "").replace(" ", "-")
        item["address"] = response.xpath('/html/body/center/div[2]/div[4]/div[3]/div[2]/dl/dd[1]/ul/li/dl/dd/text()').extract()[0]
        item["rating"] = response.xpath('/html/body/center/div[2]/div[2]/div[3]/*[@class="restGrade"]/*[@class="rate"]/*[@class="score"]/*[@class="total"]/text()').extract()[0]
        item["rest_type"] = response.xpath('/html/body/center/div[2]/div[2]/*[@class="areaBasic"]/*[@class="restType"]/*[@class="type"]/text()').extract()[0]
        item["img"] = "http://www.menupan.com" + response.xpath('//*[@id="rest_bigimg"]/@src').extract()[0]
        
        data = response.xpath('/html/body/center/div[2]/div[4]/script[5]/text()').extract()[0]
        link = "http://menupan.com" + re.findall("/[\w]+/[\w]+/[\w]+\.[\w]+\?[\w]+=[\d]+&[\w]+=[\d]+", data)[0]
        
        yield scrapy.Request(link, callback=self.parse2, cb_kwargs={'item': item})
       
    def parse2(self, response, item):
        data2 = response.xpath('/html/head/script[3]/text()').extract()[0]
        lat, lng = re.findall("[\d]+\.[\d]+", data2)
        item["lat"] = lat
        item["lng"] = lng
        yield item
```

> ### 2. 전처리 및 DB 저장
```

```
> ### 3. 이동경로 위치 수집
```
import requests
import urllib.parse as urlparse
from geopy import distance

class Route:
    def __init__(self, headers={"X-NCP-APIGW-API-KEY-ID": "czf9niiek1",
           "X-NCP-APIGW-API-KEY": "3Rf6Inv4bbf0h51YmlDRtDbgUiC2yRjfW7d0vwoO"}):
        self.headers = headers
    
    # 각 출발지 -> 위경도 변환
    def addr_to_xy(self):
        # 주소값 입력
        self.d1_name = input("출발지 1을 입력하세요. : ")
        self.d2_name = input("출발지 2를 입력하세요. : ")
        # URL 설정
        self.d1_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={}".format(self.d1_name)
        self.d2_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={}".format(self.d2_name)
        # 리퀘스트
        self.response1 = requests.get(self.d1_url, headers=self.headers)
        self.response2 = requests.get(self.d2_url, headers=self.headers)
        # JSON 파싱하여 위경도 추출
        self.d1_x = self.response1.json()["addresses"][0]["x"] 
        self.d1_y = self.response1.json()["addresses"][0]["y"]
        self.d2_x = self.response2.json()["addresses"][0]["x"]
        self.d2_y =  self.response2.json()["addresses"][0]["y"]
        return self.d1_x, self.d1_y, self.d2_x, self.d2_y
    
    # 출발지간 위경도 -> 경로값 변환
    def road_path(self):
        self.d1_xy = str(self.d1_x) + "," + str(self.d1_y)
        self.d2_xy = str(self.d2_x) + "," + str(self.d2_y)
        self.d_option = "traoptimal"
        self.d_url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={}&goal={}&option={}".format(self.d1_xy, self.d2_xy, self.d_option)
        self.response = requests.get(self.d_url, headers=self.headers)
        self.path = self.response.json()["route"]["traoptimal"][0]["path"]
        self.avg_path = self.response.json()["route"]["traoptimal"][0]["summary"]["distance"] / len(self.path)
        print("거리 : {}m, ".format(self.response.json()["route"]["traoptimal"][0]["summary"]["distance"]), len(self.path), ", ", self.avg_path)
        return self.path
    
    # 출발지간 대중교통 경로
    def trans_path(self, path_type=0):
        self.path_type = path_type
        self.key = 'lxOFkKZ6BCIrJYAQQbeuYsBW+6br+fKss6pEigRpVqA'
        self.url = 'https://api.odsay.com/v1/api/searchPubTransPathT'
        self.params = {'apiKey' : self.key,
                  'SX' : self.d1_x,
                  'SY' : self.d1_y,
                  'EX' : self.d2_x,
                  'EY' : self.d2_y,
                  'SearchPathType' : self.path_type,
                  'OPT':0,
                 }
        self.url = self.url + '?' + urlparse.urlencode(self.params)
        self.response = requests.get(self.url)
        # 경로내 정류장 위경도 추출
        self.transit_count = self.response.json()['result']['path'][0]['info']['busTransitCount'] + self.response.json()['result']['path'][0]['info']['subwayTransitCount']
        self.distance = round(self.response.json()['result']['path'][0]['info']['totalDistance'] / 1000,2)
        self.stop_lat_lng = []
        for i in range(1, 2*self.transit_count, 2):
            self.stop_info = self.response.json()['result']['path'][0]['subPath'][i]['passStopList']['stations']
            self.stop_lat_lng += [(float(a['y']),float(a['x'])) for a in self.stop_info]
        # 경로가 1km이하거나, 정류장이 5개 미만이면 모든 위경도 표출하고, 이외에는 중간 6개의 정류장 위경도만 표출
        if self.distance <= 1 or len(self.stop_lat_lng) <= 5:
            self.meet_point = self.stop_lat_lng
        else:
            self.meet_point = self.stop_lat_lng[len(self.stop_lat_lng)//2-3:len(self.stop_lat_lng)//2+3]
        print('거리: {}km'.format(self.distance))
        return self.meet_point, self.stop_lat_lng
```

> ### 4. 프론트페이지 만들기
```

```

> ### 5. DB 연동
```

```    
# 한계점

        
