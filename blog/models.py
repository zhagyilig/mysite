from django.db import models
from django.contrib.auth.models import User
from django.utils import  timezone
# Create your models here.

class BlogArticles(models.Model):
    """ 博客文章models """
    title =  models.CharField(max_length=300,verbose_name="主题")
    author = models.ForeignKey(User, related_name='blog_posts',verbose_name="作者")  # related_name属性定义名称(related_name是关联对象反向引用描述符)
    body = models.TextField(verbose_name="文章主体")
    publish = models.DateTimeField(default=timezone.now,verbose_name="出版时间")

    class Meta:
        ordering = ('-publish',)  # 以出版时间倒序展示

    def __str__(self):
        return self.title  # 显示标题字符串