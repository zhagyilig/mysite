from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    birth = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True)
    school = models.CharField(max_length=100, blank=True)  # blank=True表示该项数据可以为空,即前端界面中允许用户不填写
    company = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    photo = models.ImageField(blank=True)  # p101

    def __str__(self):
        return "user:{}".format(self.user.username)