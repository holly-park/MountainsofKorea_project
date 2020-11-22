

area = { 
"02" : "세종특별자치시",
"04" : "대구광역시",
"06" : "인천광역시",
"08" : "울산광역시",
"10" : "강원도",
"12" : "충청북도",
"14" : "전라북도",
"16" : "경상북도",
"01" : "서울특별시",
"03" : "부산광역시",
"05" : "광주광역시",
"07" : "대전광역시",
"09" : "경기도",
"11" : "충청남도",
"13" : "전라남도",
"15" : "경상남도",
"17" : "제주도"}



sample = "http://know.nifos.go.kr/openapi/mtweather/mountListSearch.do?keyValue=발급된_인증키정보&version=1.0&localArea=1&obsid=1910&tm=201508280900"

import urllib.request
import urllib
import datetime
from bs4 import BeautifulSoup
import csv
a=str(input("산이름을 입력하세요:"))
#path='/home/cloudera/Documents/Develop/mt_korea/scarp_code/wpoint.scv'
f = open('./scarp_code/testDB.csv', 'r', encoding='utf-8')
reader = csv.reader(f)
lines = list(reader)

for i in lines:
    if a == (i[0]):
        WETHER_ID =str(i[5])
        va =str(i[4])
        
        AREA=str([k for k, v in area.items() if v == va])[2:-2]                   
        #print(WETHER_ID,AREA)
        break
  
f.close()

KEY = 'Nwg3el60bnk6AH7n3Ynp83bkOwjxbrpva%2Fe8hEOvsFY%3D'
#AREA = 9 #지역 : 위의 지역 번호 참조
#ID =1891 # 관측지점 id : 첨부된 기상관측지점상세정보.csv 참조 !!!주의, 관측지점의 지역과 지역번호는 일치되어야 함.
now = datetime.datetime.now()
DATE= now.strftime('%Y%m%d')

API_HOST = f'http://know.nifos.go.kr/openapi/mtweather/mountListSearch.do?keyValue={KEY}&version=1.0&localArea={AREA}&obsid={WETHER_ID}&tm={DATE}'
#print(API_HOST)
req = urllib.request.Request(API_HOST)
data = urllib.request.urlopen(req).read()
soup = BeautifulSoup(data, features="xml")

name = str(soup.select('obsname'))[10:-11]
temp = str(soup.select('tm2m'))[7:-8]
humid = str(soup.select('hm2m'))[7:-8]
wind = str(soup.select('ws2m'))[7:-8]

print("산이름 = ",name, "온도 = ",temp,"도","습도 = ", humid,"%","풍속 =", wind,"m/s")