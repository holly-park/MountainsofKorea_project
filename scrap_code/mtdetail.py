import requests
import json
import csv
import pandas as pd

header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
b=[]
# f = open('mt_de.csv', 'w', encoding='utf-8')
for num in range (1,101):
    a=[]
    url = f'http://mtweather.nifos.go.kr/famous/mountainOne?stnId={num}'
    res = requests.get(url, headers=header).json()
    cont = res.get("famousMTSDTO")    
    mtname=cont.get("stnName")
    desc =cont.get("description")
    print(desc)
#     f.write(mtname+","+desc+"\n")
# f.close()
# f = open('mt_height.csv', 'r', encoding='utf-8')

# df_INNER_JOIN = pd.merge(b, f, left_on='mtname', right_on='mtname', how='inner')
# print(df_INNER_JOIN)
# f.close()
