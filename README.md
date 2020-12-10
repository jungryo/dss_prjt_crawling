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
```
* scrapy를 이용한 
import scrapy
import re
from menupan.items import MenupanItem

class MenupanSpider(scrapy.Spider):
    name = "Menupan"
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }
    start_urls = ["http://www.menupan.com/restaurant/bestrest/bestrest.asp?page={}&pt=wk".format(i) for i in range(1, 41)]
    # download_delay = 1
    
    def parse(self, response):
        links = response.xpath('/html/body/div/div[1]/div[1]/div[4]/div[4]/ul/li/p[1]/a/@href').extract()
        links = list(map(response.urljoin, links))
        for link in links:
            yield scrapy.Request(link, callback=self.page_parse)
            
   
    
    def page_parse(self, response):
        item = MenupanItem()
        try:
            bizhour1 = response.xpath('/html/body/center/div[2]/div[2]/div[7]/div[2]/ul[1]/li[1]/dl/dd/text()').extract()[0].replace("\r", "").replace("\n", "").replace("\t", "")
        except:
            bizhour1 = response.xpath('/html/body/center/div[2]/div[2]/div[5]/div[2]/ul[1]/li[1]/dl/dd/text()').extract()[0].replace("\r", "").replace("\n", "").replace("\t", "")
        bizhour2 = response.xpath('/html/body/center/div[2]/div[2]/*[@class="tabInfo"]/*[@class="infoTable"]/*[@class="tableTopA"]/li[3]/dl/*[@class="txt1"]/text()').extract()[0]
        item["bizhour"] = "운영시간: " + bizhour1 + "  " + "휴일: " + bizhour2
        item["name"] = response.xpath('/html/body/center/div[2]/div[2]/*[@class="areaBasic"]/*[@class="restName"]/*[@class="name"]/text()').extract()[0].replace("\xa0", "")
        item["tel"] = response.xpath('/html/body/center/div[2]/div[2]/*[@class="areaBasic"]/*[@class="restTel"]/*[@class="tel1"]/text()').extract()[0].replace("(", "").replace(")", "").replace(" ", "-")
        item["address"] = response.xpath('/html/body/center/div[2]/div[4]/div[3]/div[2]/dl/dd[1]/ul/li/dl/dd/text()').extract()[0]
        item["rating"] = response.xpath('/html/body/center/div[2]/div[2]/div[3]/*[@class="restGrade"]/*[@class="rate"]/*[@class="score"]/*[@class="total"]/text()').extract()[0]
        item["rest_type"] = response.xpath('/html/body/center/div[2]/div[2]/*[@class="areaBasic"]/*[@class="restType"]/*[@class="type"]/text()').extract()[0]
        item["img"] = "http://www.menupan.com" + response.xpath('//*[@id="rest_bigimg"]/@src').extract()[0]
        item["link"] = response.url
        
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

> ### 전처리 및 DB 저장
```

```
> ### 이동경로 위치 수집
```

```

> ### 프론트페이지 만들기
```

```

> ### DB 연동
```

```       
        
