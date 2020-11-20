{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "from fake_useragent import UserAgent"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "# driver = webdriver.Chrome()\n",
    "options = webdriver.ChromeOptions()\n",
    "options.add_argument(\"user-agent={}\".format(UserAgent().chrome))\n",
    "driver = webdriver.Chrome(options=options)\n",
    "agent = driver.execute_script(\"return navigator.userAgent;\")\n",
    "driver.get(\"https://map.naver.com/v5/subway/\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium.webdriver.common.keys import Keys"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.get(\"https://map.naver.com/v5/subway/\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.find_element_by_css_selector('#input_search_0').clear()\n",
    "driver.find_element_by_css_selector(\"#input_search_0\").send_keys(\"쌍문역\")\n",
    "driver.find_element_by_css_selector(\"#input_search_0\").send_keys(Keys.RETURN)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.find_element_by_css_selector('#input_search_1').clear()\n",
    "driver.find_element_by_css_selector(\"#input_search_1\").send_keys(\"흑석역\")\n",
    "driver.find_element_by_css_selector(\"#input_search_1\").send_keys(Keys.RETURN)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.find_element_by_css_selector(\".btn_direction.active\").click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [],
   "source": [
    "stations = driver.find_elements_by_css_selector(\"#container > subway-content > div > div.__subway-engine-transform > div.__subway-engine-layer.__subway-engine-directions > svg > text\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'수유(강북구청)'"
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "stations[1].text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['쌍문',\n",
       " '수유(강북구청)',\n",
       " '미아',\n",
       " '미아사거리',\n",
       " '길음',\n",
       " '성신여대입구',\n",
       " '한성대입구',\n",
       " '혜화',\n",
       " '동대문',\n",
       " '동대문역사문화공원',\n",
       " '충무로',\n",
       " '명동',\n",
       " '회현',\n",
       " '서울역',\n",
       " '숙대입구',\n",
       " '삼각지',\n",
       " '신용산',\n",
       " '이촌',\n",
       " '동작',\n",
       " '동작',\n",
       " '흑석']"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "station_list = []\n",
    "for station in stations:\n",
    "    if station not in station_list:\n",
    "        station_list.append(station.text)\n",
    "        \n",
    "station_list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "21"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(stations)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {},
   "outputs": [],
   "source": [
    "def route_station(dep, arr):\n",
    "    options = webdriver.ChromeOptions()\n",
    "    options.add_argument(\"user-agent={}\".format(UserAgent().chrome))\n",
    "    driver = webdriver.Chrome(options=options)\n",
    "    agent = driver.execute_script(\"return navigator.userAgent;\")\n",
    "    driver.get(\"https://map.naver.com/v5/subway/\")\n",
    "#    try: \n",
    "    #     driver.find_element_by_css_selector('#input_search_0').clear()\n",
    "    driver.find_element_by_css_selector(\"#input_search_0\").send_keys(dep)\n",
    "    driver.find_element_by_css_selector(\"#input_search_0\").send_keys(Keys.RETURN)\n",
    "#     driver.find_element_by_css_selector('#input_search_1').clear()\n",
    "    driver.find_element_by_css_selector(\"#input_search_1\").send_keys(arr)\n",
    "    driver.find_element_by_css_selector(\"#input_search_1\").send_keys(Keys.RETURN)\n",
    "    driver.find_element_by_css_selector(\".btn_direction.active\").click()\n",
    "    stations = driver.find_elements_by_css_selector(\"#container > subway-content > div > div.__subway-engine-transform > div.__subway-engine-layer.__subway-engine-directions > svg > text\")\n",
    "    station_list = []\n",
    "    for station in stations:\n",
    "        if station not in station_list:\n",
    "            station_list.append(station.text)\n",
    "    return station_list\n",
    "    driver.quit()\n",
    "#except:\n",
    "#    driver.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "route_serch = route_station(\"쌍문역\", \"아현역\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
