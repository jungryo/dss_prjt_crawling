import requests, json
import libs.path as path
import pandas as pd
from geopy import distance

def find_matzip(by, category, d1_address, d2_address, naver_id, naver_secret, odsay_key):
    if by == "자동차":
        mid_lat_max, mid_lat_min, mid_lng_max, mid_lng_min, crawling_point_c = path.address_to_xy(path.car_path, d1_address, d2_address, naver_id, naver_secret, odsay_key)
    elif by == "대중교통":
        mid_lat_max, mid_lat_min, mid_lng_max, mid_lng_min, crawling_point_c = path.address_to_xy(path.trans_path, d1_address, d2_address, naver_id, naver_secret, odsay_key)
    else:
        pass
    df = pd.read_csv('js_prepro_rest.csv', index_col=0)    
    df = df [df['category'] == category]
    # 위,경도 최대/최소 값으로 만든 사각지점에 있는 맛집리스트만 추출
    direction_square = df[(df['lat']<mid_lat_max) & (df['lat']>mid_lat_min) & (df['lng']>mid_lng_min) & (df['lng']<mid_lng_max)]
    # (위, 경도) 컬럼 만들기 
    direction_square['latlng'] = direction_square.apply(lambda x:(x['lat'], x['lng']), axis=1) 
    # 사각지점 안에서 선택 카테고리만 추출
    # 반경 1km 내 맛집 추출
    matzip=pd.DataFrame()
    for lat_lng in direction_square['latlng']:
        for point in crawling_point_c:
            dis = distance.distance(point, lat_lng).km
            if dis <= 1:
                df_1 = direction_square[direction_square['latlng'] == lat_lng]
                matzip = matzip.append(df_1)
    matzip.drop_duplicates(inplace=True)
    matzip.reset_index(drop=True, inplace=True)
    matzip = matzip.sort_values(by='rating', ascending=False).head()
    ranking = matzip[['fname', 'tel', 'addr', 'bizhour', 'category', 'menu', 'rating']]
    return ranking
