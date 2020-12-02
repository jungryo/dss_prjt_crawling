
def bluer():
    import requests
    import pandas as pd
    import time
    query_ls = pd.read_excel('./seoul_subway_station_v2.xlsx')
    query_ls = query_ls['전철역명']
    
    start = time.time()
    
    datas = []
    
    for query in query_ls:
        url = f'https://www.bluer.co.kr/api/v1/restaurants?page=0&size=30&query={query}'
        response = requests.get(url)
        chunk = response.json()['_embedded']['restaurants']
        
        for i in range(len(chunk)):
            data = {
                'station':query,
                'name':chunk[i]['headerInfo']['nameKR'],
                'category':chunk[i]['foodTypes'],
                'menu':chunk[i]['statusInfo']['menu'],
                'tel':chunk[i]['defaultInfo']['phone'],
                # 'addr':chunk[i]['juso']['jibunAddr'],
                'addr':chunk[i]['juso']['roadAddrPart1'],
                'lat':chunk[i]['gps']['latitude'],
                'lng':chunk[i]['gps']['longitude'],
                'ribbonType':chunk[i]['headerInfo']['ribbonType'],
                'menu':chunk[i]['statusInfo']['menu'],
                'priceRange':chunk[i]['statusInfo']['priceRange']
            }
            
            datas.append(data)
            
    df = pd.DataFrame(datas)
    df.to_csv('./bluer.csv')
    print(time.time() - start, 'sec')
    return df

bluer()
