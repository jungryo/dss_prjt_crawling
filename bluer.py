#!/usr/bin/env python

import requests
import json
import datetime

def send_msg(msg, WEBHOOK_URL="https://hooks.slack.com/services/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"):
    payload = {
        "channel": "#dss_prjt_crawling",
        "username": "dss_prjt_crawling",
        "text": msg,
    }
    requests.post(WEBHOOK_URL, data=json.dumps(payload))
    
    

def bluer():
    now = datetime.datetime.now()
    send_msg("{}크롤링 시작".format(now.strftime('%Y-%m-%d_%H-%M')))

    import requests
    import pandas as pd
    import time
    query_ls = pd.read_csv('./data/seoul_subway_station.csv')
    query_ls = query_ls['전철역명']
        
    datas = []
    
    for query in query_ls:
        url = f'https://www.bluer.co.kr/api/v1/restaurants?page=0&size=30&query={query}'
        response = requests.get(url)
        chunk = response.json()['_embedded']['restaurants']
        
        for i in range(len(chunk)):
            data = {
                'station':query,
                # 'thumbnail':'https://www.bluer.co.kr' + chunk[i]['firstImage']['url'],
                'id':chunk[i]['id'],
                'name':chunk[i]['headerInfo']['nameKR'],
                'category':chunk[i]['foodTypes'],
                'menu':chunk[i]['statusInfo']['menu'],
                'tel':chunk[i]['defaultInfo']['phone'],
                'addr':chunk[i]['juso']['jibunAddr'],
                # 'addr':chunk[i]['juso']['roadAddrPart1'],
                'lat':chunk[i]['gps']['latitude'],
                'lng':chunk[i]['gps']['longitude'],
                'ribbonType':chunk[i]['headerInfo']['ribbonType'],
                'menu':chunk[i]['statusInfo']['menu'],
                'priceRange':chunk[i]['statusInfo']['priceRange']
            }
            
            datas.append(data)
            
    df = pd.DataFrame(datas)
    df.to_csv('./bluer.csv')
    
    send_msg({}/{}개의 맛집 크롤링 완료".format(now.strftime('%Y-%m-%d_%H-%M'), len(df)))
    return df

bluer()
