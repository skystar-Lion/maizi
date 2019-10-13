from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from myblog.models import Article, Cateory, Comment, User
from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django import forms
from django.contrib import auth
import logging


logger = logging.getLogger('blog_log')
# Create your views here.


class UserRegister(forms.Form):
    """docstring for UserRegister"""
    username = forms.CharField(label = '用户', max_length = 30)
    password = forms.CharField(label = '密码', max_length = 30)
    qq = forms.CharField(label = 'QQ', max_length = 30)
    email = forms.CharField(label = '邮箱', max_length = 30)
        

class UserForm(forms.Form):
    """docstring for UserForm"""
    username = forms.CharField(label = '用户', max_length = 30)
    password = forms.CharField(label = '密码', max_length = 30)
        


def global_setting(request):
    return {'site_name': settings.SITE_NAME}

def index(request):
    contents = Article.objects.all().order_by('-date_published')
    con_cateory = list(Article.objects.all().values('category__name').annotate(count = Count('category'))
        .values('count','category__name').order_by('-count'))
    #获取page的请求参数，默认是1
    try:
        page = int(request.GET.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    #将数据库的查询内容每页分为4条记录返回
    ppaginator = Paginator(contents, 4)
    try:
        pagelist = ppaginator.page(page)
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        pagelist = ppaginator.page(1)
    if pagelist.number > ppaginator.num_pages - 3 and ppaginator.num_pages > 3:
        list_range = ppaginator.page_range[ppaginator.num_pages - 3:ppaginator.num_pages]
    elif ppaginator.num_pages <= 3:
        list_range = ppaginator.page_range[0:3]
    else:
        list_range = ppaginator.page_range[pagelist.number - 1:pagelist.number + 2]
    username = request.COOKIES.get('username', '')
    return render(request, 'index.html', locals())

def show_blog(request):
    if request.method == 'GET':
        try:
            title = request.GET['title']
        except:
            return render(request, '404.html')
        try:
            contents = Article.objects.get(title = title)
            con_cateory = list(Article.objects.all().values('category__name').annotate(count = Count('category'))
                .values('count','category__name').order_by('-count'))
            """
            print(Article.objects.all().values('category__name').annotate(count = Count('category'))
            .values('count','category__name').order_by('-count').query.__str__())
            """
            com_replys = Comment.objects.all().filter(article__iexact = title)
            return render(request, 'blog.html', locals())
        except:
            return HttpResponseRedirect(reverse('index'))

def addcomment(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            user_email = request.POST['email']
            content = request.POST['comment']
            title = request.POST['title']
            #print(username, user_email, content, title)
        except:
            return render(request, '404.html')
        try:
            Comment.objects.create(content = content, user = username, article = title, user_email = user_email)
            return redirect('/blog/?title=%s' % title)
        except Exception as e:
            return render(request, '404.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        """
        #auth.authenticate 是后台认证，即只有可以登录后台的长高才可以认证
        #user = auth.authenticate(username = username, password = password)
        print(user)
        if user and user.is_active:
            auth.login(request, user)
            response = HttpResponseRedirect(reverse('index'))
            return response
        """
        user = User.objects.filter(username__exact = username, password__exact = password)
        if user:
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('username', username, 3600)
            return response
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        uf = UserForm()
        return render(request, 'login.html', {'uf':uf})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        qq = request.POST['qq']
        email = request.POST['email']
        user = User.objects.create(username = username, password = password, qq = qq, email = email)
        """
        user = auth.authenticate(username = username, password = password)
        print(user)
        if user and user.is_active:
            auth.login(request, user)
            response = HttpResponseRedirect(reverse('index'))
            return response
        """
        if user:
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('username', username, 3600)
            return response
        else:
            return HttpResponseRedirect(reverse('register'))

    else:
        uf = UserRegister()
        return render(request, 'register.html', {'uf':uf})


def login_out(request):
    auth.logout(request)
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('username')
    return response
