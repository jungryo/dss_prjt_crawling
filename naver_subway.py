#!/usr/bin/env python
# coding: utf-8

# In[56]:


import requests
import pandas as pd
import scrapy
from scrapy.http import TextResponse
from fake_useragent import UserAgent


# In[57]:


def restaurant(station, displayCount = 100):
    dfs = []
    for page in range(1,4):
        url = "https://map.naver.com/v5/api/search?caller=pcweb&query={}맛집&type=all&page={}&displayCount={}&isPlaceRecommendationReplace=true&lang=ko".format(station, page, displayCount)
        headers = {'user-agent': UserAgent().chrome}
        response = requests.get(url, headers = headers)
        datas_df = pd.DataFrame(response.json()["result"]["place"]["list"])
        datas_df = datas_df[["id","name", "tel", "category", "shortAddress","bizhourInfo", "menuInfo"]]
        dfs.append(datas_df)
    
    result_df = pd.concat(dfs)
    result_df.reset_index(drop=True, inplace= True)

    ids = list(result_df['id'])
    
    id_ = []
    count = 0
    for i in ids:
        url = "https://m.place.naver.com/restaurant/{}/home".format(i)
        headers = {'cookie': 'NNB=7K4ZOLYOV6DV6; NRTK=ag#all_gr#1_ma#-2_si#0_en#0_sp#0; ASID=d3d9a4d70000017560b549fd00000058; _fbp=fb.1.1604372603371.379259291; nx_ssl=2; m_loc=eadd65b7308d6f4bfc8098ebbbdb1bae9d714a268e72c14499ebfd398a30cb9a; _ga=GA1.1.1921936816.1603073336; _ga_7VKFYR6RV1=GS1.1.1605702861.5.0.1605702861.60; nid_inf=892943255; NID_AUT=XirjxBwSSzPl2QpaB7zu/arY6xMA1js3IXkbqVfAG4HSRnpLl0+b/xDZuBhEaiZz; NID_JKL=Xx8d0kSMBC8SsWrs9/PfNl6MGi2HawSjFhBlCOs5wwM=; theme-promotion-november-notice-closed-count=1; BMR=; page_uid=UJqd8wprvmsssPH1LOCssssstis-339467; NID_SES=AAABoOs4VETPaN2WckzKIRZoqPzPko7TzXfsTOiict7BE083Hq9FplL/TYklvXPvJCTiXgB1sW4CuxEJmX+5NTFMKzS9uEDnUiNu7vMtYMS6KGnYRxcfWtKQGMLe0HAtl7hDVfT7G6CsAwmVPUtEfhQkMDW9l1i4Jp+C2Q2OFsIWxURA7TuACbLoxBfax0rWygofoc6M1rzJr27iVJpcKPr9l8s/a53aK3wgmNxqbh3kZcetbsq4MUaHbHI5hOTu4Eeoj2xKNhoJHQyUFHu8ZkDEAk4a93fNLck0cLnKR6JUWst+Z1ZIDlT4IRhnylGcnJMOlgUEGPrs32iIxLjwcdjo+BQfYEPJFsVAYd8uhZob1IZdnggPP0L4CUHuFyHTB6/V1CWIxmN66kjuv0+i8sXmV6YubPHNLcU8f0ykIzw8TqSdqsqW+ToRBlC3agO5I3iC1L/1giKfRPLgWi2qAX6Y0n1qcUc6O0x1Nnv9PUDg+9QDYGPKkFXhX/DEQVCPwXX1efNVQFxBq5yOLCLdzyIFfOdWPSHv0Cxo9GluWtvtN9da; wcs_bt=80c9a70e2db3:1606062842|sp_966c8ef1b4cae0:1606062538',
                  "user-agent": UserAgent().chrome}

        response = requests.get(url, headers = headers)
        dom = TextResponse(response.url, body = response.text, encoding = "utf-8")
        try: 
            element = dom.xpath('//*[@id="app-root"]/div/div[2]/div[1]/div/div/div[1]/div/span[1]/em/text()')[0].extract()
            id_.append(element)
        except:
            id_.append('0')
        count += 1 
    
    result_df["star"] = id_
    result_df.to_csv("station_datas/{}.csv".format(station), sep=",", index=False)
    return result_df
# 정려님이 짜신 함수 끝에 csv파일로 저장하는 코드 한 줄만 추가


# In[52]:


restaurant("성수역")


# In[58]:


station_info= pd.read_csv("seoul_subway_station.csv", encoding="euc-kr")
station_info.tail()


# In[59]:


station_list = station_info["전철역명"]


# In[60]:


station_list = list(station_list)


# In[ ]:


# 일단은 테스트를 위해 3개까지만, 3개 정도는 오류 안 나고 실행되는데 그 이상으로 가면 오류나기 시작함. 중간에 끊어지는 것 해결 해야 할 듯.
for station in station_list[:3]:
    restaurant(station+"역", displayCount = 100)  

