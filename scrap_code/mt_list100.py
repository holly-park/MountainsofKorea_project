import csv
from pymongo import MongoClient

f = open("scrap_code/mtdb.csv", "r", encoding="utf-8")
readers = csv.reader(f)

# for reader in readers:
#     print(reader)

# with MongoClient("mongodb://127.0.0.1:27017/") as client: #개인 피씨
with MongoClient("mongodb://192.168.0.171:8087/") as client: # 공용 서버
    mtdb = client["mt_db"]
    if "mt_col" not in mtdb.list_collection_names():
        mtdb.create_collection('mt_col')

    NO = ""
    NAME = ""
    ADDRESS = ""
    LAT = ""
    LON = ""
    HEIGHT = ""
    AREA = ""
    DETAIL = ""
    for reader in readers:
        NO = reader[0]
        NAME = reader[1]
        ADDRESS = reader[2]
        LAT = reader[3]
        LON = reader[4]
        HEIGHT = reader[5]
        AREA = reader[6]
        DETAIL = reader[7]
        
        data = {'NO': NO, 'NAME': NAME, 'ADDRESS': ADDRESS, 'LAT': LAT, 'LON':LON, 'HEIGHT' : HEIGHT,'AREA':AREA, 'DETAIL':DETAIL}
        mtdb.mt_col.insert_one(data)

# 172.17.0.2