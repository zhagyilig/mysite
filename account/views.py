from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login  # 内置用户认证和管理应用中引入的两个方法
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # 装饰器函数
from django.http import HttpResponseRedirect # 实现Url跳转
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserInfoForm, UserForm
from .models import UserProfile, UserInfo


def user_login(request):
    """ 用户登录验证视图 """
    if request.method == 'POST':
        login_form = LoginForm(request.POST)  # request.POST得到提交表单数据，是一个类字典对象
        if login_form.is_valid():  # 验证表单信息
            cd = login_form.cleaned_data  # 以字典的形式返回实例的具体数据，即经过校验之后的属性及其值
            user = authenticate(username=cd['username'], password=cd['password']) # 1
            if user:
                login(request, user)  # 以1所得的user实例对象作为参数，实现用户登录
                return HttpResponse('Welcome You. You have been authenticated successfully')
            else:
                return HttpResponse('Invalid login')
    if request.method == 'GET':
        login_form = LoginForm()   # 第一次向server发出含有表单页面的请求，然后反馈前端页面，等待用户输入
        return render(request, 'account/login.html', {'form': login_form})

def register(request):
    """ 用户注册视图 """
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)  # 将表单数据保存到数据库，并生成数据对象;commit=False 仅仅生成数据对象
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)  # 在保存用户注册信息后,同时在account_userinfo 数据库表写入该用户的ID信息 #93
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry,your can't register.")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        connext = {"form": user_form, "profile": userprofile_form}
        return render(request, "account/rigister.html", connext)

@login_required(login_url="/account/login/") # 将没登录的用户转到登录界面,向装饰器传参
def myself(request):
    """ 个人信息 """
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    context = {"user":user, "userinfo":userinfo, "userprofile":userprofile}
    return render(request, "account/myself.html", context)

@login_required(login_url="/account/login/")
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')  # 当用户提交了个人信息成功就页面跳转
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth, "phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school, "company":userinfo.company,
                                              "profession":userinfo.profession, "address":userinfo.address,
                                              "aboutme":userinfo.aboutme})
        context = {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form}
        return render(request, "account/myself_edit.html", context)

@login_required(login_url="/account/login/")
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, "account/imagecrop.html",)