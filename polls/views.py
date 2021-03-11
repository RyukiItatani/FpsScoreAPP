from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Record
from .form import UserForm, UserCreateForm, LoginForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from django.utils import timezone
import sqlite3
import io
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import base64
import datetime
from django.http import  HttpResponseServerError
from django.views.decorators.csrf import requires_csrf_token

#ログインview
class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/polls/new')
        return render(request, 'polls/create.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return  render(request, 'polls/create.html', {'form': form,})

create_account = Create_account.as_view()
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/polls/new')
        return render(request, 'polls/login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'polls/login.html', {'form': form,})

account_login = Account_login.as_view()

class Account_logout(View):
    def get(self, request, *args, **kwargs):
       logout(request)
       return render(request,'polls/index.html')
account_logout = Account_logout.as_view()

class Username(View):
    def get(self, request, *args,**kwargs):
        user = self.request.user
        return HttpResponse({user})
username = Username.as_view()
#HTML呼び出し関数

@login_required
def new(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST)
        record = Record.objects.create(
                                        user = request.user,
                                        kill = request.POST.get('kill'),
                                        death = request.POST.get('death'),
                                        score = request.POST.get('score'),
                                        DateTime = timezone.datetime.now()) + datetime.timedelta(hours=9)
     
    kill_graph, death_graph, score_graph, kd_graph = graph_main(user)
    my_dict = {
    'data':None,
    'header':None,
    'form':UserForm(request.POST),
    'kill_graph': kill_graph,
    'death_graph': death_graph,
    'score_graph': score_graph,
    'kd_graph': kd_graph
    }

    data = Record.objects.filter(user=user)
    header=['User','キル数','デス数','スコア数','記録日時','削除']
    my_dict['data'] = data
    my_dict['header'] = header
    return render(request, 'polls/new.html',my_dict)
#表のデータ削除
def td_del(request,td_id):
    td = Record.objects.filter(id=td_id)
    td.delete()
    return redirect('polls:new')
#グラフ作成メイン関数
def graph_main(user):
    kill_list, death_list, score_list, kd_list, week_list = create_list(user)
    for i in range(7):
        week_list[i] = week_list[i].strftime('%m-%d')
    create_graph(kill_list,week_list)
    kill_graph = get_image()
    create_graph(death_list,week_list)
    death_graph = get_image()
    create_graph(score_list,week_list)
    score_graph = get_image()
    create_graph(kd_list,week_list)
    kd_graph = get_image()
    return kill_graph, death_graph, score_graph, kd_graph
    
#以下はグラフ作成の関数群
#キル、デス、スコア、kd、日付の一週間の集計したリストを作成する
def create_list(user):
    week_list = []
    kill_list = []
    death_list = []
    score_list = []
    kd_list = []

    dt_now = datetime.date.today()

    #キル、デス、スコアのリストを二重リストにする。今日の日付から一週間分の日付をリストに保存する
    for i in range(7):
        kill_list.append(list())
        death_list.append(list())
        score_list.append(list())
        week_list.append(dt_now - datetime.timedelta(days = i))


    #今日から一週間の日付のデータをそれぞれ取得しキル、デス、スコアのリストそれぞれにデータを保存する
    for i in range(7):
        data = Record.objects.filter(DateTime__startswith=str(week_list[i],user=str(user))
        for data in data: # 0:id 1:user 2:kill 3:death 4:score 5: datetime
            kill_list[i].append(data.kill)
            death_list[i].append(data.death)
            score_list[i].append(data.score)

    

    #キル、デス、スコアのリストから日付ごとの値の平均をとり保存する
    def avg_list(list):
        for i in list:
            cnt = 0
            for j in range(len(i)):
                cnt = cnt + int(i[j])
            if len(i) != 0:
                avg = cnt/len(i)
            else:
                avg = 0
            list[list.index(i)] = avg

    avg_list(kill_list)
    avg_list(death_list)
    avg_list(score_list)

    #kdを求めリストに保存する
    for i in range(7):
        if death_list[i] != 0:
            kd = kill_list[i]/death_list[i]
        else:
            kd = 0
        kd_list.append(kd)

    return kill_list, death_list, score_list, kd_list, week_list

#グラフ作成
def create_graph(x_list,y_list):
    plt.cla()
    fig = plt.figure(figsize=(6,5))
    plt.plot(y_list,x_list,label="x",marker='^',markersize=8,color="dimgray",mfc='orange',mec='black')
    for x, y in zip(y_list, x_list):
        plt.text(x, y, round(y,2), ha='center', va='bottom')
    plt.xlabel('date')

#グラフの画像作成
def get_image():
     buffer = io.BytesIO()
     plt.savefig(buffer, format='png')
     image_png = buffer.getvalue()
     graph = base64.b64encode(image_png)
     graph = graph.decode('utf-8')
     buffer.close()
     return graph
#エラーの詳細を表示する関数
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)