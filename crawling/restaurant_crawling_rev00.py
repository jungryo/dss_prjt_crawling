# 하나의 지하철 역을 정하고, 주변 맛집과 별점 크롤링하기
def restaurant(station, displayCount = 100):
    import requests
    import pandas as pd
    import scrapy
    from scrapy.http import TextResponse
    from fake_useragent import UserAgent
    
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
    return result_df

# 내생각에 브라우저 버전이 낮으면 평점을 끌고 오지 못하는 단점이 있다.(내생각)..
