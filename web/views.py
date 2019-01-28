# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
import json
from web.myforms import MyForm, MyLoginForm
from repository import models
from utilities.my_paginator import Mypaginator
from io import BytesIO
#from django.utils.check_code import create_validate_code
#from utils.check_code import create_validate_code
from utilities.ck_code import check_code
from django.db.models import Count, Avg, Max, Min, Sum
import pymysql
from django.db import connection, connections
from django.db.models import F

def likesOrunlikes(request, *args, **kwargs):
    article_id = request.GET.get('article_id')
    print(article_id)
    if kwargs['what'] == 'likes':
        models.Article.objects.filter(id=article_id).update(upcount=F('upcount')+1)
        #likes = models.User_Article.objects.create(uid=,)
        obj = models.Article.objects.filter(id=article_id).first()
        #likes = models.User_Article.objects.filter(id=article_id,feels=1).count()
        return HttpResponse(json.dumps({'status':'ok', 'likes': obj.upcount}))
    else:
        models.Article.objects.filter(id=article_id).update(downcount=F('downcount')+1)
        obj = models.Article.objects.filter(id=article_id).first()
        #unlikes = models.User_Article.objects.filter(id=article_id, feels=0).count()
        return HttpResponse(json.dumps({'status':'ok','unlikes':obj.downcount}))

def blogcontent(request, *args, **kwargs):
    print(kwargs)
    blog = models.Blog.objects.filter(suffix=kwargs['suffix'])
    condition = kwargs['condition']
    if condition == 'tag':
        article_list = models.Article.objects.filter(tag=kwargs['condition_id'], blog=blog)
    elif condition == 'category':
        article_list = models.Article.objects.filter(classification=kwargs['condition_id'], blog=blog)
    else:
        article_list = models.Article.objects.filter(tag=kwargs['condition_id'],blog=blog)
    #return HttpResponse('ok...')
    return render(request, 'blogcontent.html', {})

def blog(request, *args, **kwargs):
    myblog = models.Blog.objects.filter(suffix=kwargs['suffix']).select_related('uid').first()
    user_obj = models.User.objects.filter(blog=myblog).first()
    if not myblog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=myblog)
    category_list = models.Classification.objects.filter(blog=myblog)
    #article_list = models.Article.objects.filter(user__username=kwargs['suffix']).order_by('-id')
    #date_list = models.Article.objects.raw('select count(ctime) as num,date_format(ctime,"%%Y-%%m") as cctime from Article group by date_format(ctime,"%%Y-%%m")')
    # date_list = models.Article.objects.aggregate(k=Count('ctime'))
    # print(date_list)

    #connection.connect()
    conn = connection.connection
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("""select count(1) as num,date_format(ctime,'%Y-%m') as cctime from Article group by date_format(ctime,'%Y-%m')""")
    date_list = cursor.fetchall()
    print(date_list)
    connection.close()

    if kwargs.get("condition", None):
        condition = kwargs['condition']
        if condition == 'tag':
            article_list = models.Article.objects.filter(tag=kwargs['condition_id'], blog=myblog)
        elif condition == 'category':
            article_list = models.Article.objects.filter(cls=kwargs['condition_id'], blog=myblog)
        else:
            article_list = models.Article.objects.filter(blog=myblog).extra(where=['date_format(ctime, "%%Y-%%m")=%s'],
                                                                            params=[kwargs['condition_id'],]
                                                                            ).all()
    else:
        article_list = []
    #blog_obj = models.Blog.objects.filter(suffix=kwargs['suffix'])[0]
    return render(request, 'blog.html',
                  {'blog_obj': myblog,
                   'user_obj': user_obj,
                   'article_list': article_list,
                   'tag_list': tag_list,
                   'category_list': category_list,
                   'date_list': date_list
                   }
                  )
    #return HttpResponse('somebody blog...')

def cktestmain(request):
    return render(request, 'checkcode.html')

def cktest(request):
    f = BytesIO()
    img, code = check_code()
    img.save(f, 'PNG')
    checkcode = f.getvalue()
    #return render(request, 'checkcode.html', locals())


    return HttpResponse(f.getvalue())


def logout(request):
    # del request.COOKIES['username']
    #request.session.clear()
    request.session.flush()
    return redirect('/')


def login(request):
    if request.method == 'GET':
        obj = MyLoginForm()
        return render(request, 'login.html', {'form': obj})
    elif request.method == 'POST':
        obj = MyLoginForm(request.POST)
        if obj.is_valid():
            user = str(obj.cleaned_data['user'])
            # pwd = str(obj.cleaned_data['pwd'])
            # print(user, pwd)
            # userobj = models.User.objects.filter(username=user)
            # print(userobj[0])
            # print(userobj.exists(), userobj[0].pwd)
            # if userobj.exists() and userobj[0].pwd == pwd:
            # res = redirect('/')
            # res.set_cookie('username', user)
            blog_obj = models.Blog.objects.filter(uid__username=user)[0]
            request.session['username'] = user
            request.session['is_login'] = True
            request.session['suffix'] = blog_obj.suffix
            request.session.set_expiry(600)
            return redirect('/')
            # else:
            #     return redirect('/login')
        else:
            #errors = obj.errors
            return render(request, 'login.html', {'form': obj})
    #return HttpResponse('It is login page that has not been set...')


def register(request):
    if request.method == 'GET':
        regForm = MyForm()
        return render(request, 'register.html', {'form': regForm})
    elif request.method == 'POST':
        regForm = MyForm(request.POST, request.FILES)
        if regForm.is_valid():
            print(regForm.cleaned_data)
            user = regForm.cleaned_data["user"]
            pwd = regForm.cleaned_data["pwd"]
            email = regForm.cleaned_data["email"]
            img = regForm.cleaned_data["img"]
            print(img.name, img.size)
            with open('./static/imgs/'+img.name, 'wb') as f:
                for line in img.chunks():
                    f.write(line)
            try:
                models.User.objects.create(
                    username=user,
                    pwd=pwd,
                    email=email,
                    img='static/imgs/'+img.name
                )
            except Exception as e:
                print(e)
            #return HttpResponse('ok...')
            # res = redirect('/')
            # res.set_cookie('username', user)
            request.session['username'] = user
            request.session['is_login'] = True
            return redirect('/')
        else:
            errors = regForm.errors
            print errors
            return render(request, 'register.html', {'form': regForm})


def index(request, *args, **kwargs):
    #user = request.COOKIES.get('username')
    #if not user:
    #    return redirect('/login')
    if not kwargs:
        baseurl = '/'
    else:
        kwargs["article_type_id"] = int(kwargs["article_type_id"])
        baseurl = reverse('home', kwargs={"article_type_id": kwargs["article_type_id"]})
    print(kwargs)
    #print(baseurl)
    article_type_list = models.Article.type_choices
    totalCount = models.Article.objects.filter(**kwargs).count()
    cp = request.GET.get("p")
    if not cp:
        currentPage = 1
    else:
        currentPage = cp
    page_obj = Mypaginator(totalCount, currentPage, 3, 7, baseurl)
    #print(page_obj.baseurl)
    data_list = models.Article.objects.filter(**kwargs)[page_obj.start:page_obj.end]
    return render(request, 'index.html',
                  {"page_obj": page_obj,
                   "data_list": data_list,
                   "article_type_list": article_type_list,
                   "kwargs": kwargs,
                   'request': request
                   })


# def index(request, *args, **kwargs):
#     # if not kwargs:
#     #     pass
#     #     # kwargs["article_type_id"] = None
#     #     # article_list = models.Article.objects.all()
#     # else:
#     #     kwargs["article_type_id"] = int(kwargs["article_type_id"])
#     print(kwargs)
#     article_list = models.Article.objects.filter(**kwargs)
#     article_type_list = models.Article.type_choices
#
#     current_page = request.GET.get('p', None)
#     if not current_page:
#         current_page = 1
#     paginator = CustomPaginator(current_page, 11, article_list, 3)
#     try:
#         posts = paginator.page(current_page)
#
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request,
#                   'index.html',
#                   {'posts': posts,
#                    'article_type_list': article_type_list,
#                    'kwargs':kwargs
#                    }
#                   )


def get_content(request):
    art_id = request.GET.get("article_id")
    content_obj = models.Article.objects.filter(id=art_id).first()

    return render(request, 'content.html', locals())


def get_mycontent(request, *args, **kwargs):
    blog_obj = models.Blog.objects.filter(suffix=kwargs['suffix']).first()
    user_obj = models.User.objects.filter(blog__suffix=kwargs['suffix']).first()
    #art_id = request.GET.get("article_id")
    art_id = kwargs.get('article_id')
    likes = models.User_Article.objects.filter(aid__id=art_id, feels=1).count()
    unlikes = models.User_Article.objects.filter(aid__id=art_id, feels=0).count()
    #print('likes:%s, unlikes:%s'%(likes, unlikes))
    content_obj = models.Article.objects.filter(id=art_id).first()
    tag_list = models.Tag.objects.filter(blog=blog_obj)
    category_list = models.Classification.objects.filter(blog=blog_obj)
    conn = connection.connection
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(
        """select count(1) as num,date_format(ctime,'%Y-%m') as cctime from Article group by date_format(ctime,'%Y-%m')""")
    date_list = cursor.fetchall()
    #print(date_list)
    connection.close()
    return render(request, 'mycontent.html',
                  {'blog_obj': blog_obj,
                   'user_obj': user_obj,
                   'tag_list': tag_list,
                   'category_list': category_list,
                   'content_obj': content_obj,
                   'date_list': date_list,
                   'likes': likes,
                   'unlikes': unlikes
                   }
                  )
