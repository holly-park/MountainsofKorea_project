import requests
import json
from pymongo import MongoClient

def getLatLng(ADDRESS):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+ADDRESS
    header = {"Authorization": "KakaoAK ee0cf33fb761c2003bf8840f07f8accc"}
    result = json.loads(str(requests.get(url,headers=header).text))
    
    match_first = result['documents'][0]['address']

    return float(match_first['y']),float(match_first['x'])

ADDRESS =    "경기도양주시백석읍 양주산성로 545"
s=getLatLng(ADDRESS)
print(s)
with MongoClient("mongodb://127.0.0.1:27017/") as client:
        gp_list = list(client.mt_db.goodp_col.find({}))