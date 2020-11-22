import time
import pymongo
from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

with MongoClient("mongodb://localhost:27017/") as client:
    gps_db = client["gps_db"]
    if "gps_collection" not in gps_db.list_collection_names():
        gps_db.create_collection('gps_collection')

        options = Options()
        options.headless = True
        browser = webdriver.Chrome(executable_path="/home/bjh/Documents/Develop/chromedriver", options=options)
        browser.get("http://bac.blackyak.com/html/challenge/ChallengeVisitList.asp?CaProgram_key=114")

        mt_data=list()
        gps_data=list()

        time.sleep(3)

        for i in range(1,101):
            mt=browser.find_elements_by_css_selector(f'#VisitRecordList > ul > li:nth-child({i}) > div > div.text > span:nth-child(1)')
            for j in mt:
                mt_data.append(j.text)

#key=['NAME', 'GPS']
for value in gps_data:
    v=value
    print(v)
    # for k,v in zip(key,value):
    #     data[k]=v
    # print(data)

