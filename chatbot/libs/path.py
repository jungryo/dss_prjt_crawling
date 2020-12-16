import requests
import json
import urllib.parse as urlparse
import pandas as pd


def address_to_xy(func, d1_address, d2_address, naver_id, naver_secret, odsay_key):
    d1_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={}".format(d1_address)
    d2_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={}".format(d2_address)
    headers = {"X-NCP-APIGW-API-KEY-ID": naver_id, 
               "X-NCP-APIGW-API-KEY": naver_secret,
              }
    # 리퀘스트
    response1 = requests.get(d1_url, headers=headers)
    response2 = requests.get(d2_url, headers=headers)
    # JSON 파싱하여 위경도 추출
    d1_x = response1.json()["addresses"][0]["x"] 
    d1_y = response1.json()["addresses"][0]["y"]
    d2_x = response2.json()["addresses"][0]["x"]
    d2_y = response2.json()["addresses"][0]['y']
    if func == car_path:
        return func(d1_x, d1_y, d2_x, d2_y, naver_id, naver_secret)
    else:
        return func(d1_x, d1_y, d2_x, d2_y, odsay_key)
    
def car_path(d1_x, d1_y, d2_x, d2_y,naver_id, naver_secret):
    # 출도착지 위경도 -> 경로내 위경도 가져오기
    d1_xy = str(d1_x) + "," + str(d1_y)
    d2_xy = str(d2_x) + "," + str(d2_y)
    d_option = "traoptimal"
    d_url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={}&goal={}&option={}".format(d1_xy, d2_xy, d_option)
    headers = {"X-NCP-APIGW-API-KEY-ID": naver_id,
               "X-NCP-APIGW-API-KEY": naver_secret,
              }
    response = requests.get(d_url, headers=headers)
    path = response.json()["route"]["traoptimal"][0]["path"]
    # 중간 경로의 모든 값
    middle_path = path[len(path)//3:int(len(path)//(3/2))]
    # 중간 경로 중 크롤링 포인트
    crawling_point = middle_path[::10]
    # 경도, 위도 -> 위도, 경도 (geopy format)
    crawling_point_c = [(i[1],i[0]) for i in crawling_point]
    # 중간경로의 위,경도 최대 최소값으로 for문 돌리는 df 사이즈 줄이기 
    mid_lng_min = min([data[0] for data in middle_path])-0.1
    mid_lng_max = max([data[0] for data in middle_path])+0.1
    mid_lat_min = min([data[1] for data in middle_path])-0.1
    mid_lat_max = max([data[1] for data in middle_path])+0.1
    return mid_lat_max, mid_lat_min, mid_lng_max, mid_lng_min, crawling_point_c

def trans_path(d1_x, d1_y, d2_x, d2_y, odsay_key):
    # 대중교통 경로 가져오기
    url = 'https://api.odsay.com/v1/api/searchPubTransPathT'
    params = {'apiKey' : odsay_key,
              'SX' : d1_x,
              'SY' : d1_y,
              'EX' : d2_x,
              'EY' : d2_y,
              'SearchPathType' :2,
              'OPT':0,
             }
    url = url + '?' + urlparse.urlencode(params)
    response = requests.get(url)
    # 경로내 정류장 위경도 추출
    transit_count = response.json()['result']['path'][0]['info']['busTransitCount'] + response.json()['result']['path'][0]['info']['subwayTransitCount']
    total_distance = round(response.json()['result']['path'][0]['info']['totalDistance'] / 1000,2)
    all_points = []
    for i in range(1, 2*transit_count, 2):
        stop_info = response.json()['result']['path'][0]['subPath'][i]['passStopList']['stations']
        all_points += [(float(a['y']),float(a['x'])) for a in stop_info]
    # 경로가 1km이하거나, 정류장이 5개 미만이면 모든 위경도 표출하고, 이외에는 중간 6개의 정류장 위경도만 표출
        if total_distance <= 1 or len(all_points) <= 5:
            crawling_point_c = all_points
        else:
            crawling_point_c = all_points[len(all_points)//2-3:len(all_points)//2+3]
    mid_lng_min = min([data[1] for data in crawling_point_c])-0.1
    mid_lng_max = max([data[1] for data in crawling_point_c])+0.1
    mid_lat_min = min([data[0] for data in crawling_point_c])-0.1
    mid_lat_max = max([data[0] for data in crawling_point_c])+0.1
    return mid_lat_max, mid_lat_min, mid_lng_max, mid_lng_min, crawling_point_c
