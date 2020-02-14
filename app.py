#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv

import os
import sys
import csv
import time
# import concurrent.futures
import asyncio
import requests

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_area(city):
    driver = webdriver.Chrome()
    area_store_dict[city] = {}
    driver.get(url_city + '?city=' + city)
    area_list_tag = driver.find_element_by_id('areaList')
    area_store_list = area_list_tag.text.split('\n')
    
    with open(dir_family + '/' + city + '.csv','w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for area in area_store_list:
            area_store_dict[city][area] = {}
            driver.get(url_area + '?city=' + city + '&area=' + area)
            road_list_tag = driver.find_element_by_id('roadList')
            road_store_list = road_list_tag.text.split('\n')
            for road in road_store_list:
                try:
                    driver.get(url_road + '?city=' + city + '&area=' + area + '&road=' + road)
                    elems = driver.find_elements_by_xpath("//a[@href]")
                    for elem in elems:
                        if 'shop_place' in elem.get_attribute("href"):
                            writer.writerow([elem.get_attribute("href")])
                except Exception as ex:
                    print(ex)
    driver.close()

async def get_area_async(city):
    res = await loop.run_in_executor(None, get_area, city)

load_dotenv()
url_index = 'https://www.hilife.com.tw/storeInquiry_street.aspx'
dir_family = './store_hilife'
city_list = [
    "台北市",
    "基隆市",
    "新北市",
    "宜蘭縣",
    "新竹縣",
    "桃園市",
    "苗栗縣",
    "台中市",
    "彰化縣",
    "南投縣",
    "嘉義縣",
    "雲林縣",
    "台南市",
    "高雄市",
    "屏東縣",
    "金門縣",
    "新竹市",
    "嘉義市",
]

## 建立資料夾
check_dir(dir_family)

## headless ##
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# executable_path = '/home/walter/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=executable_path,
# chrome_options=chrome_options)
driver = webdriver.Chrome()
driver.get(url_index)
last_city_option = ''
select_num = 0
option_num = 0

city_obj = {}
for city in city_list:
    driver.find_element_by_xpath("//select[@name='CITY']/option[text()='" + city + "']").click()
    time.sleep(0.2)
    area_element = driver.find_element_by_xpath("//select[@name='AREA']")
    area_all_options = area_element.find_elements_by_tag_name("option")
    tmp_list = []
    for area in area_all_options:
        tmp_list.append(area.text)
    city_obj[city] = tmp_list

print(city_obj)

    # area_element = driver.find_element_by_xpath("//select[@name='AREA']")
    # area_all_options = area_element.find_elements_by_tag_name("option")
    # for option in area_all_options:
    #     print(option.text)

# area_element = driver.find_element_by_xpath("//select[@name='AREA']")
# area_all_options = area_element.find_elements_by_tag_name("option")
# for option in area_all_options:
#     print(option.text)
# 同步版本
# for city in city_list:
#     get_area(city)

# 異步版本
# tasks = []
# loop = asyncio.get_event_loop()

# for city in city_list:
#     task = loop.create_task(get_area_async(city))
#     tasks.append(task)

# loop.run_until_complete(asyncio.wait(tasks))