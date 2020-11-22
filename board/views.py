from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import folium
from django.core.paginator import Paginator
import requests
import json

from django.core.paginator import Paginator

from pymongo import MongoClient
# Create your views here.

def index(request):
    #return HttpResponse("/board/list 로 가세요:)")
    return render(request, 'board/firstpage.html')   

def boardlist(request): 
   
    data = request.GET.copy()                                          # 빈 Query Dict 생성

    with MongoClient("mongodb://127.0.0.1:27017/") as client:          # MondoDB 연결
        mt_list = list(client.mt_db.mt_col.find({}))                   # DB 추출
    paginator = Paginator(mt_list, 10)                                 # 페이지네이션 
    page_number = request.GET.get('page', 1)                           # 페이지네이션
    data3 = {'page_obj' : paginator.get_page(page_number)}             # 페이지네이션 
                                                                       # 템플릿으로 넘겨주기
    return render(request, 'board/mtlist_fromdb.html', { 'page_obj' : paginator.get_page(page_number)})  

def goodpriceview(request,ADDRESS): 
    datas={}  
    with MongoClient("mongodb://127.0.0.1:27017/") as client:
        gp_list = list(client.mt_db.goodp_col.find({'ADDRESS':ADDRESS}))
        datas['gp_list'] = gp_list
        title =gp_list[0]['TITLE']
        sector =gp_list[0]['SECTOR']
        tel =gp_list[0]['TEL']
        lat=gp_list[0]['X']
        lon=gp_list[0]['Y']
        
        lat_long = [lat, lon]
        m = folium.Map(lat_long, zoom_start=10)
        popText = folium.Html(f'<b>{title}({sector})</b></br>'+f'<b>{tel}</b></br>', script=True)
        popup = folium.Popup(popText, max_width=2650, show=True)
        folium.RegularPolygonMarker(location=lat_long, popup=popup).add_to(m)
        m = m._repr_html_()
        # folium 한글 깨짐 현상 발생시 아래 패키지 설치
        # pip install git+https://github.com/python-visualization/branca.git@master
        datas['mountain_map'] = m
        
    return render(request, 'board/goodpriceview.html', context=datas)        

def boardview(request,NAME):
    datas={}
    with MongoClient("mongodb://127.0.0.1:27017/") as client:         # DB 연결해서 Data 받아올 준비
        mt_list = list(client.mt_db.mt_col.find({'NAME':NAME}))       # 상세보기에 해당하는 특정 데이터 추출
        name=mt_list[0]['NAME']                                       # NAME 변수 설정 
        height=mt_list[0]['HEIGHT']                                   # HEIGHT 변수 설정 
        area=mt_list[0]['AREA']                                       # AREA 변수 설정 
        no=mt_list[0]['NO']                                           # NO 변수 설정 
        lat=mt_list[0]['LAT']                                         # LAT 변수 설정 
        lon=mt_list[0]['LON']                                         # LON 변수 설정 
        
        lat_long = [lat, lon]
        m = folium.Map(lat_long, zoom_start=10)                       # folium 으로 Map 에 시각화 준비
        popText = folium.Html(f'<b>{name}&nbsp;({height}m)</b></br>'+f'<b>{area}</b></br>', script=True)
        popup = folium.Popup(popText, max_width=2650, show=True)                   # popup text 설정
        folium.RegularPolygonMarker(location=lat_long, popup=popup).add_to(m)      # popup marker 설정
        m = m._repr_html_() 
        header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        url = f'http://mtweather.nifos.go.kr/famous/mountainOne?stnId={no}' # 실시간 기상정보 파싱 준비
        res = requests.get(url, headers=header).json()                      # json 데이터 추출
        cont = res.get("famousMTSDTO")                                      # 데이터 가공
        weather2 = [cont.get("forestAWS10Min")]                             # 데이터 가공
        weather1 = [res.get("others")]                                      # 데이터 가공
        
        datas['mt_list'] = mt_list                                          # Dict 으로 템플릿에 넘겨줄 준비
        datas['weather1'] = weather1                                        # Dict 으로 템플릿에 넘겨줄 준비
        datas['weather2'] = weather2                                        # Dict 으로 템플릿에 넘겨줄 준비
        datas['mountain_map'] = m                                           # Dict 으로 템플릿에 넘겨줄 준비
    
    return render(request, 'board/boardview.html', context=datas)           # 템플릿에 넘겨줌


def goodpricelist(request): 
       
    data = request.GET.copy()

    with MongoClient("mongodb://127.0.0.1:27017/") as client:
        goop_list = list(client.mt_db.goodp_col.find({}))
    paginator = Paginator(goop_list, 10)
    page_number = request.GET.get('page', 1)
    data1 = {'page_obj' : paginator.get_page(page_number)}

    # return render(request, 'board/mtlist_fromdb.html', context=datas)  
    return render(request, 'board/goodprice.html', {'page_obj' : paginator.get_page(page_number)})  
