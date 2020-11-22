import requests
import json
import csv
import pandas as pd

header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
b=[]
f = open('mt_he.csv', 'w', encoding='utf-8')
for num in range (1,101):
    a=[]
    url = f'http://mtweather.nifos.go.kr/famous/mountainOne?stnId={num}'
    res = requests.get(url, headers=header).json()
    cont = res.get("famousMTSDTO")    
    mtname=cont.get("stnName")
    #a.append(mtname)  
    address=cont.get("address")
    #a.append(address)
    lat=cont.get("fmtLat")
    #a.append(lat)
    lon=cont.get("fmtLon")
    #a.append(lon)
    #desc =cont.get("description")
    #a.append(desc)
    weather2 = cont.get("forestAWS10Min")
    
    print (weather2)
    
    #f.write(str(num)+","+mtname+","+address+","+lat+","+lon+"\n")
f.close()

