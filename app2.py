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
import data

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_area(city):
    driver = webdriver.Chrome()
    driver.get(url_index)
    driver.find_element_by_xpath("//select[@name='CITY']/option[text()='" + city + "']").click()
    time.sleep(1)
    with open(dir_hilife + '/' + city + '.csv','w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['店舖名稱','地址','電話'])
        for area in data.city_obj[city]:
            driver.find_element_by_xpath("//select[@name='AREA']/option[text()='" + area + "']").click()
            tbody_tag = driver.find_elements_by_tag_name('tbody')
            for t in tbody_tag:
                if t.text:
                    t_list = t.text.split('\n')
                    i = 0
                    tmp_list = []
                    while i < len(t_list):
                        ## name
                        tmp_list.append(t_list[i])
                        ## address
                        tmp_list.append(t_list[i+1])
                        ## phone
                        tmp_list.append(t_list[i+2])
                        i += 3
                    writer.writerow(tmp_list)
            time.sleep(1)
    driver.close()

async def get_area_async(city):
    res = await loop.run_in_executor(None, get_area, city)

load_dotenv()
url_index = 'https://www.hilife.com.tw/storeInquiry_street.aspx'
dir_hilife = './store_hilife'
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
check_dir(dir_hilife)

## headless ##
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# executable_path = '/home/walter/bin/chromedriver'
# driver = webdriver.Chrome(executable_path=executable_path,
# chrome_options=chrome_options)

# 同步版本
for city in data.city_obj.keys():
    get_area(city)
    input()

# 異步版本
# tasks = []
# loop = asyncio.get_event_loop()

# for city in data.city_obj.keys():
#     task = loop.create_task(get_area_async(city))
#     tasks.append(task)

# loop.run_until_complete(asyncio.wait(tasks))