#!/usr/bin/env python
# coding: utf-8

import requests
import scrapy
from scrapy.http import TextResponse
from selenium import webdriver
import pandas as pd
import json
import time
import datetime

locations = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']
categories = ['한식', '중식', '카페', '술집', '고기집', '횟집', '해산물', '밥집', '분식,' '패스트푸드', '파스타', '뷔페', '국물요리', '면요리', '이탈리안', '프렌치', '아시안']

WEBHOOK_URL = 'https://hooks.slack.com/services/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'

def send_msg(msg, channel = "#dss", username="다이닝코드 크롤링"):
    payload = {"channel": channel, "username":username, "text":msg}
    return requests.post(WEBHOOK_URL, json.dumps(payload))

now = datetime.datetime.now()
send_msg("{}크롤링 시작".format(now.strftime('%Y-%m-%d_%H-%M')))

links = []
for location in locations:
    for category in categories:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)
        url = "https://www.diningcode.com/list.php?query={}%20{}".format(location, category)
        driver.get(url)

        count = 0    
        while count < 4:
            try: 
                driver.find_element_by_xpath('//*[@id="div_list_more"]/span').click()
                count += 1 
                time.sleep(2)
            except:
                break

        restaurants = driver.find_elements_by_css_selector('#div_list > [onmouseenter]')

        for res in restaurants:
            res_id = res.find_element_by_css_selector("a").get_attribute("href")
            links.append(res_id)
        driver.quit()
    send_msg("--{}완료--".format(location))
    
set_link = set(links)
links = list(set_link)

msg1 = "{}개의 링크 수집 완료, 정보 수집시작".format(len(links))
send_msg(msg1)

df = pd.DataFrame()
count = 0
for link in links:
    req = requests.get(link)
    response = TextResponse(req.url, body = req.text, encoding = 'utf-8')

    data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
    id_code = link[-12:]
    name = data['name']
    address = data['address']['streetAddress']
    tel= data['telephone']
    try:
        review_count = data['aggregateRating']['reviewCount']
    except:
        review_count= "None"
    if review_count == "None":
        star = "None"
    else:
        try:
            star = data['aggregateRating']['ratingValue']
        except:
            star = response.xpath('//*[@id="lbl_star_point"]/span[1]/text()')[0].extract()[:-1]
    try:
        score = response.xpath('//*[@id="div_profile"]/div[1]/div[4]/p/strong/text()')[0].extract()
    except:
        score = response.xpath('//*[@id="div_profile"]/div[1]/div[5]/p/strong/text()')[0].extract()
    try:
        zzim = response.xpath('//*[@id="div_profile"]/div[1]/div[5]/a[1]/span/i/text()')[0].extract()
    except:
        zzim = response.xpath('//*[@id="div_profile"]/div[1]/div[6]/a[1]/span/i/text()')[0].extract()
    try:
        menu = data['servesCuisine']
    except:
        menu = response.xpath('//*[@id="div_profile"]/div[1]/div[3]/a/text()').extract()
    df = df.append({
        'id': id_code,
        'name':name,
                   'address': address,
                   "tel": tel,
                   "review_count": review_count,
                   "star": star,
                   "score":score,
                   "zzim":zzim,
                   "menu":menu}, ignore_index=True)
    count+=1
    if count % 100 == 0:
        send_msg("--{}개 맛집완료--".format(count))

df.to_csv("/home/ubuntu/python3/notebook/dss_prjt_crawling/{}_diningcode.csv".format(now.strftime('%Y-%m-%d_%H-%M')))
msg2 = "{}/{}개의 맛집 크롤링 완료".format(now.strftime('%Y-%m-%d_%H-%M'),len(df))
send_msg(msg2)