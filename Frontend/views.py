from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.template.loader import get_template
from django.template import Context
import subprocess
import shlex
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User   
from django.contrib.auth import authenticate
from SmsBackEnd.models import change_contents , new_event
from SmsBackEnd.helper import deleteImage , dictfetchall  
from django.db.models import Max , F  
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger       
from django.core import serializers
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from pymongo import MongoClient

# Create your views here.


# Home page
@login_required()
def index(request):
    c = connection.cursor()  
    # get list of all project
    try:
        myclient = settings.CONNECTMONGO
        mydb = myclient["RiceDNA"]
        mycol = mydb["DT1"]

        mydoc = mycol.find()

        user_session = request.session.get('user_session')
        if request.user is not None:
            context = {     
                'user_session':user_session,
                'data':mydoc
            }
            return render(request, 'home_page.html', context)
        else:
            return redirect('/Users/login/')
    finally:
        c.close()
        print('error')



# variant page
# @login_required()
def gene(request):
       
    # get list of all project 

        myclient = settings.CONNECTMONGO
        mydb = myclient["RiceDNA"]
        mycol = mydb["DT1"]

        mydoc = mycol.find()

        context = {     
                
            'data':mydoc
        }
        return render(request, 'gene_page.html',context)

def dataManage(request):
       
    # get list of all project 
    
            return render(request, 'manage_page.html')

def sample(request):
       
    # get list of all project 
        myclient = settings.CONNECTMONGO
        mydb = myclient["RiceDNA"]
        mycol = mydb["DT1"]

        mydoc = mycol.find()

        context = {     
                
            'data':mydoc
            }
        return render(request, 'sample_page.html',context)

def profile(request):
    c = connection.cursor() 
     # get list of all project 
 

    try:
        user_id = request.session.get('user_id')
        sql = "SELECT * FROM auth_user WHERE id=%s"
        val = str(user_id)
        c.execute(sql,val)

        result = dictfetchall(c)
        context = {
            'data_user':result,
        }
        return render(request, 'profile.html', context)
        
    finally:
        c.close()
        print('error')


#แปลงเป็น Type dict
def dictfetchall(c):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in c.description]
    return[
        dict(zip(columns,row))
        for row in c.fetchall()
    ]

#ดึงข้อมูลข้าวในmongodb
def json_data(request):
    client = MongoClient('mongodb+srv://admin:1234@ricedna.sj3ht.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = client["RiceDNA"]
    collection = db["DT1"]
    myquery = { 'CHROM': 'chr1'}
    data = collection.find(myquery)   
    # return JsonResponse(list(data), safe=False)
    # return JsonResponse(data={'data': list(data)})
    # data_cle = list()
    data_AC = list()
    # data_AF = list()
    # data_AN = list()
    for x in data:
        # del x['INFO']
        # data_cle.append(x)
        
        data_AC.append(x['INFO']['AC'])
        # data_AF.append(x['INFO']['AF'])
        # data_AN.append(x['INFO']['AN'])
    # return JsonResponse(data_cle, safe=False)
    return JsonResponse(data={
        'data_AC': data_AC
        # 'data_AF': data_AF,
        # 'data_AN': data_AN,
    })


# def json_data2(request):
#     client = MongoClient('mongodb+srv://admin:1234@ricedna.sj3ht.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
#     db = client["RiceDNA"]
#     collection = db["DT2"]
#     myquery = { 'CHROM': 'chr1'}
#     data2 = collection.find(myquery)   
#     # return JsonResponse(list(data), safe=False)
#     # return JsonResponse(data={'data': list(data)})
#     # data2_cle = list()
#     data2_AC = list()
#     data2_AF = list()
#     data2_AN = list()
#     for x in data2:
#         # del x['INFO']
#         # data_cle.append(x)
#         data2_AC.append(x['INFO']['AC'])
#         data2_AF.append(x['INFO']['AF'])
#         data2_AN.append(x['INFO']['AN'])
#     # return JsonResponse(data_cle, safe=False)
#     return JsonResponse(data2={
#         'data2_AC': data2_AC,
#         'data2_AF': data2_AF,
#         'data2_AN': data2_AN,
#     })

