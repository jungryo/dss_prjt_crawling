import requests
from selenium import webdriver

locations = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구', 
            '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구']
categories = ['한식', '중식', '카페', '술집', '고기집', '횟집', '해산물', '밥집', '분식,' '패스트푸드', '파스타', '뷔페', '국물요리', '면요리',
            '이탈리안', '프렌치', '아시안']

for location in locations:
    print("{}시작".format(location))

    for category in categories:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)
        url = "https://www.diningcode.com/list.php?query={}%20{}".format(
            location, category)
        driver.get(url)

        while True:
            try:
                driver.find_element_by_xpath(
                    '//*[@id="div_list_more"]/span').click()
                time.sleep(1)
            except:
                break

        restaurants = driver.find_elements_by_css_selector(
            '#div_list > [onmouseenter]')

        for restaurant in restaurants:
            name = restaurant.find_element_by_css_selector(
                'a > span.btxt').text.split(" ")[1]
            menu = restaurant.find_element_by_css_selector(
                'a > span.stxt').text
            try:
                address = restaurant.find_element_by_css_selector(
                    'a > span:nth-child(5)').text
            except:
                address = restaurant.find_element_by_css_selector(
                    'a > span:nth-child(4)').text
            zzim = restaurant.find_element_by_css_selector(
                'p > span.favor.button').text
            score = restaurant.find_element_by_css_selector(
                'p > span.point').text
            df = df.append({"name": name,
                            "menu": menu,
                            "address": address,
                            "zzim": zzim,
                            "score": score, }, ignore_index=True)
        driver.quit()
        print("{}, {}".format(location, category))
        
df.to_csv("df_jrl.csv")