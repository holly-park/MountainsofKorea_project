import requests
import json
import csv
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient

def getLatLng(ADDRESS):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+ADDRESS
    header = {"Authorization": "KakaoAK ee0cf33fb761c2003bf8840f07f8accc"}
    result = json.loads(str(requests.get(url,headers=header).text))   
    # print(result)
    if result['meta']['total_count'] != 0:
        X = result['documents'][0]['x']
        Y = result['documents'][0]['y']        
    else:
        Y=34.69498889
        X=125.20195        
    return Y,X

header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
n=1
while n<12500:
    url = f"https://www.goodprice.go.kr/search/storeview.do?bestStoreSeq={n}"
    res = requests.get(url, headers=header)
    soup = BeautifulSoup(res.content, features='xml')
    error = soup.select('title')
    
    if error[0].text == "행정안전부 착한가격업소":
        
        title = soup.select('.tit2')
        info = soup.select('span')
        #alt = soup.select('.npoint')
        TITLE = title[0].text
        ADDRESS = info[4].text
        TEL = info[6].text
        SECTOR = info[8].text
        MAIN = info[10].text
        MEMO = info[12].text
        DELIV = info[-2].text
        PARK = info[-1].text
        X,Y=getLatLng(ADDRESS)
        # with MongoClient("mongodb://127.0.0.1:27017/") as client: #개인 피씨
        with MongoClient("mongodb://192.168.0.171:8087/") as client: # 공용 서버
            mtdb = client["mt_db"]
            if "goodp_col" not in mtdb.list_collection_names():
                mtdb.create_collection("goodp_col")
            data = {'TITLE':TITLE,'TEL':TEL,'ADDRESS': ADDRESS,'X':X,'Y':Y, 'SECTOR': SECTOR, 'MAIN':MAIN, 'MEMO': MEMO,'DELIV':DELIV, 'PARK':PARK}
            mtdb.goodp_col.insert_one(data)    
            print (f"DB inserted {n}")
        n=n+1
    
    else: 
        n+=1 
        
print ("end")
   
