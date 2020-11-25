#!/usr/bin/env python
# coding: utf-8

# In[70]:


restaurant_df = pd.DataFrame(columns=["name", "phone_number", "full_address", "rating", "review_count", "latitude", "longitude", "thumbnail"])
count=0
while True:
    url = "https://stage.mangoplate.com/api/v5/top_lists/list.json?    language=kor&device_uuid=b80AC160552906941809739YYaL&device_type=web&start_index={}&request_count=20".format(count)
    response = requests.get(url)
    datas = response.json()
    if datas:
        for data in datas:
            link = data['share_url']
            link = link.split("/")[4]
            k = 0
            while k < 51:
                url_2 = "https://stage.mangoplate.com/api/v2/web/top_lists/{}/restaurants.js?                language=kor&device_uuid=b80AC160552906941809739YYaL&device_type=web&start_index={}&request_count=50".format(link, k)
                response = requests.get(url_2)
                datas2 = response.json()
                if datas2:
                    for data2 in datas2:
                        r_data = {
                        "latitude" : data2['restaurant']['latitude'],
                        "longitude" : data2['restaurant']['longitude'],
                        "phone_number" : data2['restaurant']['phone_number'],
                        "name" : data2['restaurant']['name'],
                        "review_count" : data2['restaurant']['review_count'],
                        "rating" : data2['restaurant']['rating'],
                        "full_address" : data2['restaurant']['full_address'],
                        #"comment" : data2['featured_reviews'][0]['comment'],
                        "thumbnail" : 'https://mp-seoul-image-production-s3.mangoplate.com' + "/" + data2['restaurant']['picture_url']
                        }
                        restaurant_df.loc[len(restaurant_df)] = r_data        
                        k += 50
                else: 
                    continue

        count += 20
        print("c")
    else:
        break
        
restaurant_df


# In[72]:


restaurant_df.to_csv("MangoPlate_csv/mangoplate_toplist.csv", sep=",", index=False)


# In[75]:


toplist_df = pd.read_csv("MangoPlate_csv/mangoplate_toplist.csv")


# In[76]:


toplist_df

