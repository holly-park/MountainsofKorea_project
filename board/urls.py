from django.contrib import admin
from django.urls import path, include

from . import views
app_name = 'board'

urlpatterns = [
    path('', views.index),
    path('list/', views.boardlist, name='boardlist'),                                        # 명산 리스트
    path('list/detail/<str:NAME>', views.boardview, name='boardview'),                       # 명산 상세보기
    path('goodpricelist/', views.goodpricelist, name='goodpricelist'),                       # 맛집 리스트 
    path('goodpricelist/detail/<str:ADDRESS>', views.goodpriceview, name='goodpriceview'),   # 맛집 상세보기
]