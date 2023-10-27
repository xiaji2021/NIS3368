from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordChangeView

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    # 用户退出
    path('logout/', views.user_logout, name='logout'),
    # 用户注册
    path('register/', views.user_register, name='register'),
    # 用户删除
    path('delete/<int:id>/', views.user_delete, name='delete'),
    # 修改密码
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('change_password_done/', auth_views.PasswordChangeDoneView.as_view(), name='change_password_done'),

    

]