from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.models import User
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required
from captcha.models import CaptchaStore
from .forms import ChangePasswordForm

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data

            # 验证验证码
            captcha_id = request.POST.get('captcha_0', '')
            captcha_value = request.POST.get('captcha_1', '')
            try:
                captcha_id = int(captcha_id)
            except ValueError:
                return HttpResponse("验证码不正确，请重新输入.")
            
            if CaptchaStore.objects.filter(id=captcha_id, response=captcha_value).exists():
                # 验证通过，执行账号密码验证
                user = authenticate(username=data['username'], password=data['password'])
                if user:
                    # 验证通过，执行登录
                    login(request, user)
                    return redirect("myfiles:file_list")
                else:
                    return HttpResponse("账号或密码输入有误。请重新输入~")
            else:
                return HttpResponse("验证码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

    
# 用户退出
def user_logout(request):
    logout(request)
    return redirect("myfiles:file_list")

# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("myfiles:file_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

# 删除用户
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            #退出登录，删除数据并返回博客列表
            logout(request)
            user.delete()
            return redirect("myfiles:file_list")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")
    
# 修改密码
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            
            # 验证用户的帐号和原密码
            user = authenticate(username=username, password=old_password)
            if user is not None:
                # 帐号和原密码匹配，更新密码
                user.set_password(new_password)
                user.save()
                return redirect("userprofile:login")
            else:
                return HttpResponse("原密码和帐号不匹配。")
    else:
        form = ChangePasswordForm()
    return render(request, 'userprofile/change_password.html', {'form': form})