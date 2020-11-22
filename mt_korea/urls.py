from django.contrib import admin
from django.urls import path, include

from board import views as boardview
from board import views as detailview 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', boardview.index),
    path('board/', include('board.urls')),
    
]
