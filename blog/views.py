from django.shortcuts import render, get_object_or_404
from .models import BlogArticles
# Create your views here.

def blog_title(request):
    ''' 打印文章标题 '''
    blogs = BlogArticles.objects.all()
    """
    >>> from blog.models import  BlogArticles
    >>> test = BlogArticles.objects.all()
    >>> for n in test:
    ...     print(n.id,n)
    ...
    1 面向对象的高级用法
    3 文件处理及异常
    2 装饰器
    """
    context = {"blogs":blogs}
    return render(request, 'blog/title.html', context)

def blog_article(request, article_id):
    ''' 博客文章 '''
    article = get_object_or_404(BlogArticles,id=article_id)
    pub = article.publish
    context = {'article':article, 'publish':pub}
    return render(request,'blog/content.html', context)