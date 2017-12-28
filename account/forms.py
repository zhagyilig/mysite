#!/usr/local/bin/python3
#coding=utf-8
#Author: www.xtrdb.net

from django import forms
from django.contrib.auth.models import User # django默认用户模型User类 #p63
from .models import UserProfile, UserInfo

class LoginForm(forms.Form):
    """ 用户登录表单,forms.Form不会修改数据库 """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    """ 用户注册,forms.ModelForm会修改数据库 #p63 """
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Pssword", widget=forms.PasswordInput)

    class Meta:
        """ 内部类,声明表单所应用的数据模型，也就是将来表单中的数据写入数据库表或修改某些字段值 """
        model = User
        fields = ("username", "email")   # 所选用的字段

    def clean_password2(self):
        """ 重新定义密码，且比对用户输入密码 """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']

class UserProfileForm(forms.ModelForm):
    """ 增加注册要求字段 """
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")

class UserInfoForm(forms.ModelForm):
    """ 用户个人信息 """ #p90
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme","photo",)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)