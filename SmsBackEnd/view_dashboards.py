from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import EmailMessage
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django import forms
from django.views.generic import View
from SmsBackEnd.utils import render_to_pdf

from django.views import View
from .models import *
from django.db.models import Q
from Users.models import UserSession, Profile
from django.contrib.sessions.models import Session
import django_excel as excel
import time
import datetime

import json
from django.db import connection
from django.db.models import Q  # check !=
from .helper import date_format, encode, decode, dictfetchall
from collections import Counter
import collections

# function main for user group collector
@login_required()
def smsbackend_main_collector(request):
    try:
        user_session = request.session.get('user_session')
        if user_session == 'Worker':
            breadcrumb = ['Home', 'Specimen', 'Carana']

            cursor = connection.cursor()
            cursor.execute('SELECT fw.original_code, fw.scientific_name, fw.date,rc.raw_code_text, sm.*,au.first_name FROM SmsBackEnd_specimen sm RIGHT JOIN SmsBackEnd_raw_code rc ON sm.raw_code_id = rc.id LEFT JOIN auth_user au ON sm.user_id = au.id LEFT JOIN SmsBackEnd_fieldwork fw ON fw.specimen_id = sm.id ORDER BY sm.id ASC')
            specimen_list = dictfetchall(cursor)
            count_specimen_collection = specimen.objects.filter(~Q(form_fieldwork_status='0')).count()
            count_seed_collection = specimen.objects.filter(~Q(form_fieldwork_status='0') | ~Q(form_assessment_status='0')).count()
            count_seed_preparation = specimen.objects.filter(~Q(form_seed_clean_status='0')).count()
            count_seed_germination = specimen.objects.filter(~Q(form_seed_germination_status='0')).count()
            count_seed_morphology = specimen.objects.filter(~Q(form_seed_morphology_status='0')).count()
            count_seed_storage = specimen.objects.filter(~Q(form_storage_status='0')).count()
            for i in specimen_list:
                encode_id = encode(i['id'])
                i['id'] = encode_id
            content = {
                'specimen': specimen_list,
                'count_specimen_collection':count_specimen_collection,
                'count_seed_collection':count_seed_collection,
                'count_seed_preparation':count_seed_preparation,
                'count_seed_germination':count_seed_germination,
                'count_seed_morphology':count_seed_morphology,
                'count_seed_storage':count_seed_storage
            }
            return render(request, 'dashboards/smsbackend_main_collector.html', content)
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main collector ===')


# function main for user group curator
@login_required()
def smsbackend_main_curator(request):
    try:
        print("ok header")
        user_session = request.session.get('user_session')
        if user_session == 'SuperAdmin' or user_session == 'Curator':

            if request.method == 'POST':

                type_chart = request.POST.get('type_chart','')
                type_check = request.POST.get('type_check','')

                if type_chart == 'bar_chart':
                    input_year = request.POST.get('year','')
                    input_month = request.POST.get('month','')
                    month_name = request.POST.get('month_name','')
                    year_name = request.POST.get('year_name','')
                    data = []

                    if(input_year and input_month):
                        data = [["วัน", "Plants", "Microbe", "Human", "Animal"]]
                        day = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

                        set_data = []
                        num_day = 1
                        for i_day in day:
                            plant_count = get_data = specimen.objects.filter(date_create__year=input_year,date_create__month = str(input_month).zfill(2),date_create__day = str(num_day).zfill(2)).values('date_create').count()
                            num_day += 1
                            data.append([i_day,plant_count,0,0,0,0])

                    elif(input_year):
                        data = [["เดือน", "Plants", "Microbe", "Human", "Animal"]]
                        month = [["01","ม.ค."],["02","ก.พ."],["03","มี.ค."],["04","เม.ย."],["05","พ.ค."],["06","มิ.ย."],["07","ก.ค."],["08","ส.ค."],["09","ก.ย."],["10","ต.ค."],["11","พ.ย."],["12","ธ.ค."]]
                        set_data = []
                        num = 1
                        for i in month:
                            plant_count = get_data = specimen.objects.filter(date_create__year=input_year,date_create__month = str(num).zfill(2)).values('date_create').count()
                            num += 1
                            data.append([i[1],plant_count,0,0,0,0])
                    elif(month_name):
                        data = [["วัน", "Plants", "Microbe", "Human", "Animal"]]
                        month = [["01","ม.ค."],["02","ก.พ."],["03","มี.ค."],["04","เม.ย."],["05","พ.ค."],["06","มิ.ย."],["07","ก.ค."],["08","ส.ค."],["09","ก.ย."],["10","ต.ค."],["11","พ.ย."],["12","ธ.ค."]]
                        day = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

                        set_data = []
                        num_day = 1
                        import random
                        for month_index in month:
                            if month_index[1] == month_name:
                                month_set_option = month_index[0]
                                for i_day in day:
                                    plant_count = get_data = specimen.objects.filter(date_create__year=year_name,date_create__month = str(month_index[0]).zfill(2),date_create__day = str(num_day).zfill(2)).values('date_create').count()
                                    num_day += 1
                                    ran1 = random.randint(0, 20)
                                    ran2 = random.randint(0, 20)
                                    ran3 = random.randint(0, 20)
                                    ran4 = random.randint(0, 20)

                                    # data.append([i_day,plant_count,0,0,0,0])
                                    data.append([i_day,plant_count,ran1,ran2,ran3,ran4])
                        data.append(month_set_option)

                    else:
                        get_data = ''
                    return HttpResponse(json.dumps(data))
                elif type_chart == 'pie_chart':
                    if type_check == 'plants':
                        province_name = []
                        specimen_id = []
                        geo_from_page = request.POST.get('geo_from_page','')
                        geo_data = th_geographies.objects.filter(name = geo_from_page).values('id')
                        geo_id = geo_data[0]['id']
                        province_data = th_provinces.objects.filter(geography_id = geo_id).values('name_th')
                        for i in province_data:
                            province_name.append(i['name_th'])
                        specimen_data = plant_assessment.objects.filter(province__in = province_name).values('specimen_id')
                        for i in specimen_data:
                            specimen_id.append(i['specimen_id'])
                        print("ok1")
                        geo_count_seed = seed_lab.objects.filter(specimen_id__in = specimen_id).count()
                        geo_count_molecular = molecular_lab.objects.filter(specimen_id__in = specimen_id).count()
                        geo_count_tissue = tissue_lab.objects.filter(specimen_id__in = specimen_id).count()
                        geo_count_herbarium = herbarium_lab.objects.filter(specimen_id__in = specimen_id).count()
                        geo_count = []
                        geo_count.append(geo_count_seed)
                        geo_count.append(geo_count_molecular)
                        geo_count.append(geo_count_tissue)
                        geo_count.append(geo_count_herbarium)
                        print("ok2")
                        map_data = plant_assessment.objects.all()
                        province_data = []
                        province_data2 = []
                        province_data3 = []
                        for i in map_data:
                            geo = th_provinces.objects.filter(name_th = i.province).filter(geography_id = geo_id)
                            for o in geo:
                                province_data.append(o.name_th)
                        province_data = dict(Counter(province_data))
                        for i in province_data:
                            province_data2.append(i)
                            province_data3.append(province_data[i])
                        province_data = []
                        province_data.append(province_data2)
                        province_data.append(province_data3)
                        province_data.append(geo_count)
                        return HttpResponse(json.dumps(province_data))
                        print("ok3")
                elif type_chart == 'pie_chart2':
                    if type_check == 'plants':
                        province_name = []
                        specimen_id = []
                        province_from_page = request.POST.get('province_from_page','')
                        specimen_data = plant_assessment.objects.filter(province = province_from_page).values('specimen_id')
                        for i in specimen_data:
                            specimen_id.append(i['specimen_id'])

                        province_count_seed = seed_lab.objects.filter(specimen_id__in = specimen_id).count()
                        province_count_molecular = molecular_lab.objects.filter(specimen_id__in = specimen_id).count()
                        province_count_tissue = tissue_lab.objects.filter(specimen_id__in = specimen_id).count()
                        province_count_herbarium = herbarium_lab.objects.filter(specimen_id__in = specimen_id).count()
                        province_count = []
                        province_count.append(province_count_seed)
                        province_count.append(province_count_molecular)
                        province_count.append(province_count_tissue)
                        province_count.append(province_count_herbarium)
                        print(province_count)
                        return HttpResponse(json.dumps(province_count))
                elif type_chart == 'set_goal':
                    type_specimen = request.POST.get('type_specimen','')
                    goal_lab_data = request.POST.get('goal_lab_data','')
                    goal_lab_data = goal_lab_data.split(',')

                    if type_specimen == 'plants':
                        goal_lab.objects.filter(id=1).update(
                            goal_lab_seed = goal_lab_data[0],
                            goal_lab_molecular = goal_lab_data[1],
                            goal_lab_tissue = goal_lab_data[2],
                            goal_lab_herbarium = goal_lab_data[3]
                        )
                        data = goal_lab.objects.filter(id=1).values('goal_lab_seed','goal_lab_molecular','goal_lab_tissue','goal_lab_herbarium')
                        return HttpResponse(json.dumps(data[0]))
                    return HttpResponse('ok')
                    

            else:

                # Count All Data Start ---------------------------------------------
                # count_plant = specimen.objects.filter(specimen_type = 'plant').count()
                # count_microbe = specimen.objects.filter(specimen_type = 'microbe').count()
                # count_human = specimen.objects.filter(specimen_type = 'human').count()
                # count_animal = specimen.objects.filter(specimen_type = 'animal').count()

                count_seed = seed_lab.objects.all().count()
                count_molecular = molecular_lab.objects.all().count()
                count_tissue = tissue_lab.objects.all().count()
                count_herbarium = herbarium_lab.objects.all().count()

                ### bug when no input province
                # map pie chart --------------------------------
                map_data = plant_assessment.objects.all()
                plant_geo_data = []
                plant_geo_data1 = []
                plant_geo_data2 = []
                plant_geo_data3 = [0,0,0,0,0,0]

                # for i in map_data:
                #     geo = th_provinces.objects.filter(name_th = i.province).values('geography_id')
                #     geo_id = geo[0]['geography_id']
                #     geo = th_geographies.objects.filter(id = geo_id).values('name')
                #     plant_geo_data2.append(geo[0]['name'])
                #     count1,count2,count3,count4,count5,count6 = 0,0,0,0,0,0
                counter=collections.Counter(plant_geo_data2)
                plant_geo_data2 = []

                for i,v in enumerate(counter):
                    plant_geo_data1.append(v)
                    plant_geo_data2.append(counter[v])
                plant_geo_data.append(plant_geo_data1)
                plant_geo_data.append(plant_geo_data2)

                # map ---------------------------------------------
                herbarium_lab_data =herbarium_lab.objects.all().values('specimen_id')
                molecular_lab_data =molecular_lab.objects.all().values('specimen_id')
                seed_lab_data =seed_lab.objects.all().values('specimen_id')
                tissue_lab_data =tissue_lab.objects.all().values('specimen_id')
                def aa(data ,color, type):
                    array = [] 
                    create_map = []
                    for i in data:
                        array.append(i['specimen_id'])
                    data = plant_assessment.objects.filter(specimen_id__in = array)
                    for i in data:
                        create_data = []
                        create_data.extend([i.latitude, i.longitude, i.province, color, type])
                        create_map.append(create_data)
                    return create_map
                herbarium_lab_data = aa(herbarium_lab_data, 'blue', 'herbarium')
                molecular_lab_data = aa(molecular_lab_data, 'red', 'molecular')
                seed_lab_data = aa(seed_lab_data, 'yellow', 'seed')
                tissue_lab_data = aa(tissue_lab_data, 'violet', 'tissue')
                create_map = []
                create_map.append(herbarium_lab_data)
                create_map.append(molecular_lab_data)
                create_map.append(seed_lab_data)
                create_map.append(tissue_lab_data)

                # get year bar_chart ---------------------------------------------
                all_year = specimen.objects.all().values('date_create')
                year = []
                for i in all_year:
                    year.append(str(i['date_create']).split('-')[0])
                year = list(dict.fromkeys(year))

                # get data lab stages PLANT ---------------------------------------              
                def get_data_stages(lab,stages):
                    num = 12
                    array = []
                    for i in range(num):
                        count = 0
                        i += 1
                        i = "{:02d}".format(i)
                        for lab_date in lab:
                            if stages == 'collect':
                                if str(lab_date['date_create']).split('-')[1] == i:
                                    count += 1
                            elif stages == 'lab':
                                if str(lab_date['date_send']).split('-')[1] == i:
                                    count += 1
                        array.append(count)
                    return array

                # collect_plant = specimen.objects.filter(specimen_type = 'plant').values()
                # collect_plant = ['d','d']
                # collect_plant = get_data_stages(collect_plant, 'collect')

                lab_seed = seed_lab.objects.all().values('date_send')
                lab_molecular = molecular_lab.objects.all().values('date_send')
                lab_tissue = tissue_lab.objects.all().values('date_send')
                lab_herbarium = herbarium_lab.objects.all().values('date_send')

                lab_seed = get_data_stages(lab_seed,'lab')
                lab_molecular = get_data_stages(lab_molecular,'lab')
                lab_tissue = get_data_stages(lab_tissue,'lab')
                lab_herbarium = get_data_stages(lab_herbarium,'lab')
                
                lab_test_data = [0,0,0,0,0,0,0,0,0,0,0,0]
                collect = []
                lab = []
                brooks = []
                test = []
                lab.extend([lab_seed,lab_molecular,lab_tissue,lab_herbarium])
                brooks.extend([lab_test_data,lab_test_data,lab_test_data,lab_test_data])
                test.extend([lab_test_data,lab_test_data,lab_test_data,lab_test_data])

                stages_plant = [10,lab,brooks,test]

                # -----------------------------------------------------------------------
                lab_plant = ['seed', 'molecular', 'tissue', 'herbarium']
                lab_microbe = ['lab1', 'lab2', 'lab3', 'lab4','lab5']
                goal_specimen = goal_lab.objects.filter(id=1).values()

                # goal_lab_plant = [goal_specimen[0]['goal_lab_seed'],goal_specimen[0]['goal_lab_molecular'],goal_specimen[0]['goal_lab_tissue'],goal_specimen[0]['goal_lab_herbarium']]

                goal_lab_microbe = [11,12,13,14,15]
                goal_lab_human = []
                goal_lab_animal = []

                # notifications
                log_list = logs.objects.all()[:5]

                content = {
                    'count_plant': 0,
                    'count_microbe': 0,
                    'count_human': 0,
                    'count_animal': 0,
                    
                    'goal_lab_plant':1,
                    'goal_lab_microbe':goal_lab_microbe,
                    'goal_lab_human':goal_lab_human,
                    'goal_lab_animal':goal_lab_animal,

                    'lab_plant': lab_plant,
                    'count_seed': count_seed,
                    'count_molecular': count_molecular,
                    'count_tissue': count_tissue,
                    'count_herbarium': count_herbarium,

                    'lab_microbe':lab_microbe,
                    'stages_plant': stages_plant,

                    'year': year,
                    'create_map':create_map,

                    # map
                    'plant_geo_data':plant_geo_data,
                    'log_list':log_list
                }
                
                return render(request, 'dashboards/smsbackend_main_curator.html', content)
        else:
            return redirect('/Users/login/')
    except Exception as e:  # contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main curator ===')

# function main for user group admin
    
def smsbackend_main_admin(request):
    try:
        user_session = request.session.get('user_session')
        cursor = connection.cursor()
        if user_session == 'SuperAdmin' or user_session == 'Curator' or user_session == 'Worker' or user_session == 'User':
            if request.method == 'POST':
                session = request.POST.get('session','')
                if session:
                    session = decode(session)
                    UserSession.objects.filter(session_id = session).delete()
                    Session.objects.filter(session_key = session).delete()

                cursor.execute(
                    'select man_session.user_id, user.username, man_session.last_login, man_session.session_id ,onlin_user.last_activity\
                    from auth_user user, Users_usersession man_session ,online_users_onlineuseractivity onlin_user\
                    where man_session.user_id = user.id AND\
                    onlin_user.user_id = user.id \
                    order by man_session.last_login, user.username'
                )
                users_online = []

                for row in cursor.fetchall():
                    online = []
                    for index, value in enumerate(row):
                        if index in [2,4]:
                            online.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                        elif index == 3:
                            online.append(encode(value))
                        else:
                            online.append(value)
                    users_online.append(online)
                return HttpResponse([users_online])
            else:
                
                
                content = {}
                return render(request, 'dashboards/smsbackend_main_admin.html',content)
        else:
            return redirect('/Users/login/')
    except Exception as e: #contains my own custom exception raising with custom messages.
        return HttpResponseServerError(e)
    finally:
        print('=== end ibiobank main ===')
