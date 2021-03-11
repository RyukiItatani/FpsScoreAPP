from django.urls import path
from polls import views
from django.contrib.auth import login, logout

app_name="polls"
urlpatterns = [
    path('new', views.new, name='new'),
    path('',views.account_login,name='login'),
    path('logout',views.account_logout,name='logout'),
    path('create',views.create_account,name='create_account'),
    path('user',views.username,name='name'),
    path('del/<int:td_id>',views.td_del,name='td_del'),
    path('test_login',views.test_login, name='test_login')

]

