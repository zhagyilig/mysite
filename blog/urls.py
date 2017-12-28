from django.conf.urls import url
from . import views

urlpatterns = [
    # name: 在写模板时,name能直接调用url:{{ blog:blog_title }},name不能重复
    url(r'^$', views.blog_title, name='blog_title'),
    url(r'(?P<article_id>\d)/$', views.blog_article, name='blog_detail'),
]
