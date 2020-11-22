from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm
import os
import time
import json
from common.CommonPage import dictfetchall, CommonPage
from django.db import connection
from .models import CoMmon 
from django.contrib.auth.decorators import login_required

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('common:login')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def base(request):
    return render(request, "index.html")

@login_required(login_url='common:login')
def index(request):
    return render(request, "./common/index.html")


def get_today():
    now = time.localtime()
    s = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    s2 = "%04d%02d%02d_%02d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    return s, s2+".png"
    
def make_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)



from django.db import connection
@csrf_exempt   #csrf 토큰 에러 제거
def save(request):
    if (request.method == 'POST'):
        dron_id = request.POST.get('dron_id')   #드론넘버
        x = request.POST.get('x')               #X좌표
        y = request.POST.get('y')               #Y좌표
        address = request.POST.get('address_name')  #주소
        img_name = request.POST.get('img_name')      #이미지 받아오기
        ip_address = request.META.get('REMOTE_ADDR') #IP주소

        print(img_name)
        #폴더 만들고, /upload/2020/09/14/20200914_1234.png
        root_dir = "./upload"
        path, filename = get_today()
        work_dir = root_dir + "/" + path
        print(work_dir)
        
        make_folder(work_dir)

        #이미지저장 20200914_1234.png
        img_name = img_name.replace('data:image/png;base64,', '') #이미지이름  
        img_name = img_name.replace(' ', '+')                                
        d = base64.b64decode(img_name)   #base64방식으로 디코딩 작업
        file = open(work_dir+"/"+ filename, mode="wb")   #wb (b가 바이너리이기 때문에 꼭 써야 저장됨)
        file.write(d)
        file.close()
       

        #DB - 일련번호, 드론식별값, 이미지 path, 이미지명, 저장된 날짜시간분초, 상대방 IP
        cursor = connection.cursor()
        sql = f"""
        insert into common_common (date, time, dron_id, x, y, address, 
        img_name, ip_address, wdate) values ('{path}', now(), '{dron_id}', '{x}', '{y}', '{address}',
         '{filename}', '{request.META['REMOTE_ADDR']}', now())
        """      
        print(sql)
        cursor.execute(sql)
        
    return HttpResponse("saved")


@login_required(login_url='common:login')
def list(request):
    #int(request.GET.get('page', '1'))
    sel = request.GET.get('sel')
    key = request.GET.get('key')

    if sel == None : sel="1"
    if key == None : key=""
    
    if sel =="1":
        cond = f" where date like '%{key}%'  or dron_id = '%{key}%' "
    elif sel=="2":
        cond = f" where date like '%{key}%' " 
    elif sel=="3":
        cond = f" where dron_id like '%{key}%' " 
    else: 
        cond = " "

    cursor = connection.cursor()
    sql ="select count(*) from common_common " + cond
    cursor.execute(sql)
    totalCount = int(cursor.fetchone()[0]) #첫번째값 가져오기
    #http://127.0.0.1:8000/board/list?page=1
    curPage = int(request.GET.get('page','1'))
    #앞에 파리미터 (page)가 값이 지정되지 않으면 기본값을 줄 수 있다.
    #curPage = request.GET['page']

    commonPage = CommonPage(totalCount, curPage, 10)
    #데이터 가져올 위치값
    start = (curPage-1)*10 #페이지가 0부터 시작하므로 0~9->실제페이지:(1-10), 10~19(11-20)
    
    sql =f'''
    select id, img_name, dron_id, date, time, ip_address, date_format(wdate, '%Y-%m-%d %T') wdate
    from common_common {cond}
    order by id desc limit {start}, 10
    '''
    #limit 시작위치, 개수
    cursor = connection.cursor()
    cursor.execute(sql)       
    common_list = dictfetchall(cursor)
    #print(common_list)
     
    context = {'common_list':common_list, 'commonPage':commonPage, 'sel':sel, 'key':key,'page':curPage}
    return render(request, 'common/common_list.html', context)


@login_required(login_url='common:login') 
def view(request, id): # 게시판 항목을 누 르면 개별 항목에 대한 것을 볼 수 있게 하기
    #id2 = request.GET['id']
    #최신 : <a href="/board/view/1">제목1</a>
    
    page= int(request.GET.get('page', '1'))
    sel = request.GET.get('sel')
    key = request.GET.get('key')

    if sel == None : sel="1"
    if key == None : key=""


    
    
    cursor = connection.cursor()
              
    sql = f"""
    select id, img_name, dron_id, date, time, wdate, x, y, address, ip_address
    from common_common
    where id={id}
    """
    cursor.execute(sql)       
    common_item = dictfetchall(cursor)    
    context = {'id':id, 'common_item':common_item[0], 'sel':sel, 'key':key, 'page':page}
    return render(request, 'common/common_view.html', context)

from django.shortcuts import get_object_or_404

def delete(request, id):
    board_obj = get_object_or_404(CoMmon, pk=id) ####### 
    board_obj.delete()
    return redirect('common:common_list')    


@csrf_exempt
def deleteall(request):
    if (request.method == 'POST'):
        cursor = connection.cursor()

        data = request.POST.get('myJSON')
        ids = json.loads(data)
        print(ids)
        q = ', '.join(ids)
        print(q)
        sql = '''
                DELETE FROM common_common WHERE id IN ({})
            '''.format(q)

        print(sql)

        cursor.execute(sql)

    return redirect('common:common_list')
   