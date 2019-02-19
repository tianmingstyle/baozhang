# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from repository import models
from django.db.models import Count, Max, Min
from forms import TroubleCreate, Trouble_kill
import datetime
# Create your views here.
def index(request):
    return redirect('/backend/trouble-list.html')
    #return render(request, 'backmanage1.html')

def trouble_list(request):
    current_user = request.session.get('username')
    #print(current_user)
    uid = models.User.objects.filter(username=current_user).first()
    trouble_list = models.Baozhang.objects.filter(uid=uid).only('id','title', 'status','ctime', 'uid', 'processor')
    return render(request,
                  'trouble-list.html',
                  {'trouble_list': trouble_list}
                  )

def trouble_create(request):

    if request.method == 'GET':
        form = TroubleCreate()
        #print(form.title)
        return render(request, 'trouble-create.html', {'form': form})
    else:
        print(11111111111111111111111111)
        print(request.session.get('username'))
        form = TroubleCreate(request.POST)
        if form.is_valid():
            current_obj = models.User.objects.filter(username=request.session.get('username')).first()
            print(current_obj)
            form.cleaned_data['uid'] = current_obj
            print(222222222222222222)
            try:
                models.Baozhang.objects.create(**form.cleaned_data)
                return redirect('/backend/trouble-list.html')
            except Exception as e:
                print(e)
        return render(request, 'trouble-create.html', {'form': form})


class MyExc(Exception):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        super(MyExc, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.msg

    def __repr__(self):
        self.__repr__ = self.__str__


class Trouble_Del(Exception):
    '''
        some EXCEPTION when del trouble.
    '''
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        super(Trouble_Del, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.msg

    def __repr__(self):
        self.__repr__ = self.__str__

def trouble_edit(request, *args, **kwargs):
    nid = int(kwargs['nid'])
    #print(nid)
    if request.method == 'GET':

        #cur_trouble = models.Baozhang.objects.filter(id=nid).values('title', 'detail').first()
        cur_trouble = models.Baozhang.objects.filter(id=nid, status=1).only('title', 'detail').first()
        #print(cur_trouble)
        #print(type(cur_trouble))
        #print(cur_trouble['title'], cur_trouble['detail'])
        if not cur_trouble:
            return HttpResponse('this case is processing or finished')
        #加入初始化参数后，可以让form不经过验证。
        form = TroubleCreate(initial={'title':cur_trouble.title, 'detail':cur_trouble.detail})
        #执行error会执行验证
        return render(request, 'trouble-edit.html', {'form': form, 'nid':nid})
    else:

        form = TroubleCreate(request.POST)
        if form.is_valid():
            try:
                v= models.Baozhang.objects.filter(id=nid, status=1).update(**form.cleaned_data)
                print(v, type(v))
                # print('i am here')
                # if  v != 1:
                #     print(44444444444444)
                #     raise MyExc('the length of title you input is too long...')
                #     #return HttpResponse('this case is processing or finished')
                # print(3333333333333333333)
            except Exception as e:
                return HttpResponse('已处理的或正在处理的报障单无法修改')
            return redirect('/backend/trouble-list.html')
        # except Exception as e:
        #     print(e)
        #     return HttpResponse(e)

        render(request, 'trouble-edit.html', {'form': form, 'nid': nid})


def trouble_delete(request, *args, **kwargs):
    nid = kwargs['nid']
    try:
        v = models.Baozhang.objects.filter(id=nid).delete()
        #print(v[0])
        if not v[0]:
            raise Trouble_Del('This trouble case maybe not exists...')
    except Trouble_Del as e:
        return HttpResponse(e)
    return redirect('/backend/trouble-list.html')



def trouble_kill_list(request):
    from django.db.models import Q
    current_id = 2 #admin
    obj = models.Baozhang.objects.filter(Q(processor_id=current_id) | Q(status=1)).order_by('status')
    return render(request, 'backend-trouble-kill-list.html', {'obj': obj})

def trouble_detail(request, nid):
    obj = models.Baozhang.objects.filter(id=nid).values('detail').first()
    #print(obj)
    return render(request, 'backend-trouble-detail.html', {'obj': obj})



def trouble_kill(request, nid):
    current_id = 2
    if request.method == 'GET':
        if models.Baozhang.objects.filter(id=nid, processor_id=current_id, status=2).exists():
            obj = models.Baozhang.objects.filter(id=nid, status=2, processor_id=current_id).only('title', 'detail',
                                                                                                 'solution').first()
            form = Trouble_kill(initial={'title': obj.title, 'detail': obj.detail, 'solution': obj.solution})
            return render(request, 'trouble-kill.html', {'form': form, 'nid': nid})
        v = models.Baozhang.objects.filter(id=nid, status=1).update(status=2, processor_id= current_id)
        #print(v)
        if not v:
            return HttpResponse('This case is grabed by other')
        obj = models.Baozhang.objects.filter(id=nid, status=2, processor_id=current_id).only('title', 'detail', 'solution').first()
        form = Trouble_kill(initial={'title':obj.title, 'detail':obj.detail, 'solution': obj.solution})
        return render(request, 'trouble-kill.html', {'form': form, 'nid': nid})

    else:
        form = Trouble_kill(request.POST)
        if form.is_valid():
            models.Baozhang.objects.filter(id=nid, status=2, processor_id=current_id).update(
                status=3,
                solution=form.cleaned_data['solution'],
                process_time=datetime.datetime.now()
            )
            return redirect('/backend/trouble-kill-list.html')
        return render(request, 'trouble-kill.html', {'form': form, 'nid': nid})
    #return HttpResponse('抢单成功')


def trouble_kill_solution(request, nid):
    obj = models.Baozhang.objects.filter(id=nid).only('solution').first()
    return render(request, 'backend-trouble-solution.html', {'obj': obj})

def highchartstest(request):
    return render(request, 'highchartstest1.html')

# def highcharts_data_by_ajax(request):
#     data = [{'name':'tianming', 'data':[10000,20000,30000,40000,50000]}, {'name':'shupeng', 'data':[
#         1000,2000,3000,4000,5000
#     ]}]
#     import json
#     return HttpResponse(json.dumps(data))


# def highcharts_data_by_ajax(request):
#     article_list = models.Article.objects.values('user_id').annotate(userCount=Count('user_id'))
#     print(list(article_list))
#     # data = [{'name': 'tianming', 'data': [10000, 20000, 30000, 40000, 50000]}, {'name': 'shupeng', 'data': [
#     #     1000, 2000, 3000, 4000, 5000
#     # ]}]
#     diclist=[]
#     dic = {}
#     for article in article_list:
#         #name = None
#         data = []
#         for k in article.keys():
#             if k == u'user_id':
#                 name = article[k]
#                 dic['name'] = name
#             if k == 'userCount':
#                 data.append(article[k])
#                 #data = d[k]
#                 dic['data'] = data
#
#         print(dic)
#         import copy
#         diic = copy.deepcopy(dic)
#         diclist.append(diic)
#
#     import json
#     print(diclist)
#     return HttpResponse(json.dumps(diclist))

def highcharts_data_by_ajax(request):
    #article_list = models.Article.objects.values('user_id').annotate(userCount=Count('user_id'))
    #print(list(article_list))
    # data = [{'name': 'tianming', 'data': [10000, 20000, 30000, 40000, 50000]}, {'name': 'shupeng', 'data': [
    #     1000, 2000, 3000, 4000, 5000
    # ]}]
    import pymysql
    from django.db import connection, connections
    connection.connect()
    conn = connection.connection
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    user_list = models.User.objects.all()
    response = []
    for user in user_list:


    #sql 统计每个用户在不同月章数量
    # seluser_id, count(user_id) from tb  group by user_id
        cursor.execute("""select count(id), date_format(ctime,'%%Y-%%m') from Article where user_id=%s group by date_format(ctime,'%%Y-%%m')""",(user.id,))
        #cursor.execute("""select strftime(ctime,'%%Y-%%m'), count(id) as cc from Article where user_id=%s group by(strftime(ctime,'%%Y-%%m'))""",(user.id,))
        row = cursor.fetchall()
        print(row)
        #print([ row[0]['t'], row[0]['cc']])
        #print([ row[0][k] for k in row[0].keys()])
        # print(row[0].keys())
        # for k in row[0].keys():
        #     print(row[0][k])
        temp = {
            'name': user.username,
            'data': [ x.values().reverse() for x in row]
            #'data': row
        }
        response.append(temp)
    connection.close()
    print(response)
    #response = [{u'data': [[u'2019-02',7],[u'2019-03',7],[u'2019-06',8]], u'name': u'tianming'}, {u'data': [[2,u'2019-02']], u'name': u'admin'}, {u'data': [[1,u'2019-03']], u'name': u'root'}]
    import json
    #print(response)
    return HttpResponse(json.dumps(response))