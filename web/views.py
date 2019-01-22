# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from web.myforms import MyForm, MyLoginForm
from repository import models
from utilities.my_paginator import Mypaginator
from io import BytesIO
#from django.utils.check_code import create_validate_code
#from utils.check_code import create_validate_code
from utilities.ck_code import check_code

def blog(request, *args, **kwargs):
    article_list = models.Article.objects.filter(user__username=kwargs['suffix'])
    blog_obj = models.Blog.objects.filter(suffix=kwargs['suffix'])[0]
    return render(request, 'blog.html',
                  {'blog_obj': blog_obj,
                   'article_list': article_list
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


def get_mycontent(request):
    art_id = request.GET.get("article_id")
    content_obj = models.Article.objects.filter(id=art_id).first()

    return render(request, 'mycontent.html', locals())