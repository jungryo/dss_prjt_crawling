import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.http import TextResponse
import json
from selenium import webdriver
import re
import time

key = '41664e4d6c69747334304c4a554542'
url = "http://openapi.seoul.go.kr:8088/{}/json/SearchSTNBySubwayLineInfo/1/730///".format(key)
response = requests.get(url)
station_infos = response.json()['SearchSTNBySubwayLineInfo']['row']
station_names = station_infos[0]['STATION_NM']
station_lines = station_infos[0]['LINE_NUM']

df_subway = pd.DataFrame(columns=["line","name"])
line_list = []
name_list = []
for station_info in station_infos:
    line = station_info['LINE_NUM']
    name = station_info["STATION_NM"]
    df_subway = df_subway.append({'line':line,
                      'name':name,}, ignore_index = True)

df_subway.sort_values(["line"], inplace=True)
df_subway.reset_index(drop=True, inplace=True)
df_subway_line2 = df_subway[df_subway["line"] == "02호선"]
df_subway_line2.reset_index(drop=True, inplace=True)


id_list_line2 =[]
for row_num in range(0, df_subway_line2["name"].count()):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    station = "{}역".format(df_subway_line2.iloc[row_num]["name"])
    url = "https://www.diningcode.com/list.php?query={}".format(station)
    driver.get(url)

    while True:
        try:
            driver.find_element_by_css_selector("#div_list_more > span").click()
            time.sleep(1)
        except:
            break
    restaurants = driver.find_elements_by_css_selector('#div_list > [onmouseenter]')
    for restaurant in restaurants:
        res_id = restaurant.find_element_by_css_selector("a").get_attribute("href")[-12:]
        id_list_line2.append(res_id)  
    driver.quit()
    
count = 0 
for i in id_list_line2:
    url = 'https://www.diningcode.com/profile.php?rid={}'.format(i)
    response = requests.get(url)
    tr_obj = TextResponse(response.url, body = response.text, encoding = 'utf-8')
    try:
        name = tr_obj.xpath('//*[@id="div_profile"]/div[1]/div[2]/p/text()')[0].extract()
    except:
        name = tr_obj.xpath('//*[@id="div_profile"]/div[1]/div[3]/p/text()')[0].extract()
    
    try:
        address = tr_obj.xpath('//*[@id="div_profile"]/div[2]/ul/li[1]/text()')[0].extract()
    except:
        address = "정보없음"
    try:
        tel = tr_obj.xpath('//*[@id="div_profile"]/div[2]/ul/li[2]/text()')[0].extract()
    except:
        tel = "정보없음"
    try:
        score = tr_obj.xpath('//*[@id="div_profile"]/div[1]/div[4]/p/strong/text()')[0].extract()
    except:
        score = "Nan"
    try:
        count_evaluation = tr_obj.xpath('//*[@id="div_profile"]/div[1]/div[4]/p/span[1]/text()')[0]\
    .extract().replace("\r","").replace("\n","").replace("\t","")[:2]
        count_evaluation= re.findall("[\d]+",count_evaluation)[0]
    except:
        count_evaluation = "평가자 없음"
    try:
        star = tr_obj.xpath('//*[@id="lbl_star_point"]/span[1]/text()')[0].extract()
        star = re.findall("\d.\d", star)[0]
    except:
        star = "Nan"
    df = df.append({"name": name,
              "address": address,
              "tel": tel,
              "score": score,
              "count_evaluation": count_evaluation,
              "star":star,}, ignore_index=True)
    count +=1

df
df.to_csv("diningcode_subway_line2.csv")