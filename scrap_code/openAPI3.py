import requests
name=str(input("산이름을 입력하세요 :"))
url = f'http://apis.data.go.kr/1400000/service/cultureInfoService/mntInfoOpenAPI?serviceKey=cRhBhi3sxVClCIks%2FemvBBGZgcYv5HaKvFr26Ov5Q5nor0WtrgUNO9rwfYO6FkLUif9SefP0BK%2B18mBFvV8%2FCw%3D%3D&searchWrd={name}'

response = requests.get(url)
print(response.status_code)
print(response.text)

import bs4
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.content, 'html.parser')
data = soup.find_all('item')

for item in data:
    mntiname = item.find('mntiname')
    mntiadd = item.find('mntiadd')
    mntidetails = item.find('mntidetails')
    mntiadmin = item.find('mntiadmin')
    mntiadminnum = item.find('mntiadminnum')
    
    print(mntiname.get_text())
    print(mntiadd.get_text())
    print(mntiadmin.get_text())
    print(mntiadminnum.get_text())
    print(mntidetails.get_text())
  