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
```python
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
>
> * 전처리 순서 
> 1. 각 사이트 별로 크롤링한 데이터 중복값 제거
> 2. 각 사이트 별 데이터 merge 
> 3. 음식점 종류에 따라 카테고리화 
> 4. 각 사이트별 별점을 5점을 기준으로 환산, null값은 각 사이트의 최소값으로 채움 
> 5. 각 사이트의 매출액을 기준으로 별점에 가중치를 두어 자체 별점 생성  
*********
  
  **별점 전처리 및 DB 저장**
```python
# 네이버 점수 변환
df[df.n_rating == 'FALSE'] = np.nan

# 블루리본서베이 점수 변환
df[df.b_rating == 'RIBBON_THREE'] = 5.
df[df.b_rating == 'RIBBON_TWO'] = 4.5
df[df.b_rating == 'RIBBON_ONE'] = 4.
df[df.b_rating == 'ATTENTION'] = 3.5
df[df.b_rating == 'NEW'] = 3.
df[df.b_rating == 'NOT'] = 3.

# 다이닝코드 점수 변환
df.d_rating = df.d_rating.str.replace('점', '')
df = df.astype({'n_rating':float, 'b_rating':float, 'd_rating':float})
df.d_rating = df.d_rating / 20.

# rating 결측값 채우기(mean)
df = df.fillna({'n_rating':df.n_rating.mean(),
              'b_rating':df.b_rating.mean(),
              'mg_rating':df.mg_rating.mean(),
              'd_rating':df.d_rating.mean(),
              'mn_rating':df.mn_rating.mean()})

# rating 반올림(소수점 둘째자리)
df.n_rating = df.n_rating.round(2)
df.b_rating = df.b_rating.round(2)
df.mg_rating = df.mg_rating.round(2)
df.d_rating = df.d_rating.round(2)
df.mn_rating = df.mn_rating.round(2)

# rating 통합
df['rating'] = (df.n_rating*.5) + (df.b_rating*.175) + (df.mg_rating*.25) + (df.d_rating*.075) + (df.mn_rating*0.01)
df.rating = df.rating.round(2)

# DB에 저장
client = pymongo.MongoClient("mongodb://user:pw@IP주소/")
restaurant = client.crawling.restaurant
items = df.to_dict("records")
restaurant.insert(items)
```
> ### 3. 이동경로 위치 수집
> * 네이버 API와 ODsay API를 이용하여 각 출발지의 위, 경도값과 출발지 두 지점을 잇는 경로에서 약 40m 지점 마다의 위, 경도값 추출
*******
```python
import requests
import urllib.parse as urlparse
from geopy import distance

class Route:
    def __init__(self, headers={"X-NCP-APIGW-API-KEY-ID": "your_API_KEY_ID",
           "X-NCP-APIGW-API-KEY": "your_API_KEY"}):
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
        self.key = 'your_key'
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
> * 지도를 보여주기 위해 카카오 API에 나와있는 예시를 활용했다.
*********
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>우리 지금 만나, 당장 만나!</title>
    
</head>
<body>
<div id="map" style="width:100%;height:100vh;"></div>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey=your_appkey"></script>
<script>
var mapContainer = document.getElementById('map'),  
    mapOption = { 
        center: new kakao.maps.LatLng(37.5657, 126.9769), 
        level: 4 
    };
var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다
var positions = [
    {
        content: '<div>시청역</div>', 
        latlng: new kakao.maps.LatLng(37.5657, 126.9769)
    },
    {
        content: '<div>덕수궁</div>', 
        latlng: new kakao.maps.LatLng(37.5658, 126.9751)
    },
    {
        content: '<div>정동길</div>', 
        latlng: new kakao.maps.LatLng(37.5669, 126.9708)
    },
    {
        content: '<div>경찰박물관</div>',
        latlng: new kakao.maps.LatLng(37.5690, 126.9697)
    }
];

for (var i = 0; i < positions.length; i ++) {
    var marker = new kakao.maps.Marker({
        map: map, 
        position: positions[i].latlng
    });

    var infowindow = new kakao.maps.InfoWindow({
        content: positions[i].content 
    });
    kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow));
    kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
}
function makeOverListener(map, marker, infowindow) {
    return function() {
        infowindow.open(map, marker);
    };
}
function makeOutListener(infowindow) {
    return function() {
        infowindow.close();
    };
}
</script>
</body>
</html>
``` 

# 현재까지 진행된 부분
* 크론탭을 이용하여 DB베이스에 주기적으로 맛집 데이터를 수집.
* 웹페이지에 특정 두 지점을 지도에 표현.  

![경로 내 맛집 추천 서비스](https://user-images.githubusercontent.com/72811950/101766454-2a55e380-3b26-11eb-8527-1d6a69795119.png)

* 처음 목표였던 시각화를 위해 파이썬 패키지인 folium 패키지를 활용.
```python
map_seoul = folium.Map(location=[37.5530, 126.9726], zoom_start=16)

for i in df_seoul.index:
     # 행 우선 접근 방식으로 값 추출하기
    name = df_seoul.loc[i, 'name']
    addr = df_seoul.loc[i, "addr"]
    tel = df_seoul.loc[i, "tel"]
    category = df_seoul.loc[i, "category"]
    bizhour = df_seoul.loc[i, "bizhour"]
    rating = df_seoul.loc[i, 'rating']
    n_rating = df_seoul.loc[i, 'n_rating']
    b_rating = df_seoul.loc[i, 'b_rating']
    mg_rating = df_seoul.loc[i, 'mg_rating']
    d_rating = df_seoul.loc[i, 'd_rating']
    mn_rating = df_seoul.loc[i, 'mn_rating']
    lat = df_seoul.loc[i, 'lat']
    lng = df_seoul.loc[i, 'lng']
    img = df_seoul.loc[i, "img"]
    
    html = '''
    이름 : {}<br>
    주소 : {}<br>
    전화번호 : {}<br>
    음식종류 : {}<br>
    영업시간 : {}<br>
    *****당장 만나야 하는 우리의 별점***** : {}<br>
    네이버 별점 : {}<br>
    블루리본 별점 : {}<br>
    망고플레이트 별점 : {}<br>
    다이닝코드 별점 : {}<br>
    메뉴판 별점 : {}<br>
    <img src="{}" alt="이미지" width="400" />
    '''.format(name, addr, tel, category, bizhour, n_rating, b_rating, mg_rating, d_rating, mn_rating, rating, img)
    
    iframe = folium.IFrame(html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)
    marker = folium.Marker([lat,lng], popup=popup)
    marker.add_to(map_seoul)
    
map_seoul
```
<img src="https://user-images.githubusercontent.com/72811950/101767655-db10b280-3b27-11eb-8890-769a6cc56392.png" width="600" height="400"></img>  
* 정보 전달을 위해 slack프로그램을 이용함.  
출발지1, 출발지2, 이동수단, 음식종류를 입력하면 전처리 된 데이터에서 별점을 기준으로  
1위부터 5위에 있는 음식점을 추천해 주는 챗봇을 만듦.  
  
**챗봇 메시지 전송 코드**
```
import requests, json

def send_msg(webhook_url, mag, channel="#dss", username="맛집찾아봇"):
    payload = {"channel":channel, "username":username, "text":mag}
    requests.post(webhook_url, data = json.dumps(payload))
```
```python
from flask import *
import libs.roadmatzip as roadmatzip
import libs.slack as slack
import time

app = Flask(__name__)
naver_id= "your_id"
naver_secret = "your_secret_key"
odsay_key = "your_key"
webhook_url = 'your_url'

@app.route("/")
def index():
    return "server is running!"

@app.route("/bot", methods=["POST"])
def bot():
    username = request.form.get("user_name")
    token = request.form.get("token")
    text = request.form.get('text')
    print(username, token, text)
    text = text.replace("matzip! ", "")
    if len(text.split("/")) != 4:
        slack.send_msg(webhook_url, "'주소1/주소2/교통수단/음식카테고리' 형식으로 입력해주세요.")
        slack.send_msg(webhook_url, "(교통수단:자동차, 대중교통 /음식카테고리:한식, 양식, 디저트, 일식, 바, 중식, 분식, 기타, 동남아식, 뷔페)")
        return Response(), 200
    
    add1, add2, by, category = text.split("/")[0], text.split("/")[1], text.split("/")[2], text.split("/")[3]
    
    if by == "자동차":
        msg = roadmatzip.addr_to_xy(roadmatzip.road_path, add1, add2, category)
        slack.send_msg(webhook_url, "{}경로 내 {} 맛집 당장만나별점 top5".format(by, category))
        time.sleep(1)
        for i in range(5):
            slack.send_msg(webhook_url, "{}위: {}, {}, {}".format((i+1), msg.iloc[i, 0], msg.iloc[i, 6], msg.iloc[i, 2]))
            time.sleep(1)
    elif by == "대중교통":
        msg = roadmatzip.addr_to_xy(roadmatzip.trans_path, add1, add2, category)
        slack.send_msg(webhook_url, "{}경로 내 {} 맛집 당장만나별점 top5".format(by, category))
        time.sleep(1)
        for i in range(5):
            slack.send_msg(webhook_url, "{}위: {}, {}, {}".format((i+1), msg.iloc[i, 0], msg.iloc[i, 6], msg.iloc[i, 2]))
            time.sleep(1)

    return Response(), 200
app.run(debug = True)
```
  
  <img src="https://user-images.githubusercontent.com/72811950/101849962-1d73d700-3b9c-11eb-933f-7e7f0653ffda.png" width="360" height="500"></img>
<img src="https://user-images.githubusercontent.com/72811950/101849983-2795d580-3b9c-11eb-8275-f2abfc18b554.png" width="450" height="350"></img>

## 아쉬웠던 점
* 데이터베이스 활용 부족.  
크롤링 프로젝트의 목적이었던 데이터베이스의 활용이 잘 이뤄지지 않았다.  
서버를 이용하여 수집된 데이터들을 자유자재로 데이터베이스에 적재하고 꺼내 쓸 수 있도록 시작되었던 프로젝트의  
목적과는 달리 단순히 데이터를 저장하기만 했고 데이터를 저장하는 것도 잘 이뤄지지 않았다.  
* flask 공부 미흡  
웹페이지 구현을 위해 공부가 필요했던 부분이었는데 개념 단계에서 더 이상 발전되지 못하였다.  
그래서 웹페이지를 제작하고 싶었던 조원들의 처음 목표를 달성하지 못했다.  
* 프론트엔드 구현 
지도상에 음식점의 위치를 표시하는 것을 목표로 프로젝트를 진행하였으나, 
DB에서 데이터를 가져와 javascript 언어로 웹페이지에 표현하는 부분이 어려웠다.  
좌표를 일일히 입력하는 것이 아니라 DB에서 선택된 데이터만 마커로 표시하는 함수를 구현하기 어려워고  
MongoDB와 javascript를 연결하는 어댑터가 필요하다는 것을 늦게 알게 되어 프로젝트 기간내에 해결하지 못했다.

## 프로젝트 완성을 위해 개선할 점
* 웹서버의 동작 원리를 충분히 이해하고 flask 패키지 공부 필요.
* 프론트엔드 언어인 html, css, javascript에 대한 기본적인 이해 필요.

### 피드백 
* DB자체 backup 기능과 동기화 기능을 이용할 수 있다.
* DB에서 데이터 select시 query문을 사용하면 더 빠르게 가져올 수 있다.
* 아이디어는 좋으니 현재까지 진행된 것을 잘 통합시켜서 서비스 하면 좋을 것 같다.

