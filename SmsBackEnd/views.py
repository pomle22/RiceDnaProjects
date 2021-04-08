from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, HttpResponseServerError , JsonResponse ,HttpResponseBadRequest ,HttpResponseRedirect,Http404
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
from .forms import AdminSignUpForm
from .form import PostForm , EventForm , SignupForm , AboutForm
from .helper import date_format, encode, decode, dictfetchall, rename_to_upload_photo, deleteImage
from PIL import Image
from .models import *
from SmsBaseApp.models import *
from django.db.models import Q
from django.http.response import JsonResponse
import os
from .helper import *
import django_excel as excel
import time, datetime  , json
from django.db.models import Max, Count
from django.db import connection
from django.dispatch import receiver
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django.views import View
adminpath = "/SmsBackEnd/manage_news_events_new"

class AuthorList(View):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)


class AuthorDetail(View):
    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        serializer = AuthorSerializer(author)
        return JsonResponse(serializer.data)


class BookDetail(View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data)


class BookList(View):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)
 

# Create your views here.
@login_required()
def manage_news_events_new(request):
     context = {}
 
     queryset = Post.objects.all().order_by('-created_on')
     paginator = Paginator(queryset, 5)
     page = request.GET.get('page')
     try:
         posts = paginator.page(page)
     except PageNotAnInteger:
         posts = paginator.page(1)
     except EmptyPage:
         posts = paginator.page(paginator.num_pages)
     
     querySearchPost = request.GET.get('q')
     if querySearchPost:
         posts = queryset.filter(
             Q(title__icontains=querySearchPost) |
             Q(content__icontains=querySearchPost) 
             
         
             )
     query = Event.objects.all()
     paginator1 = Paginator(query,5)
     page1 = request.GET.get('page1')
     try:
         events = paginator1.page(page1)
     except PageNotAnInteger:
         events = paginator1.page(1)
     except EmptyPage:
         events = paginator1.page(paginator1.num_pages)
     
    
     
     
     queryContact = Contact.objects.all()
     paginator2 = Paginator(queryContact,5)
     page2 = request.GET.get('page2')
     try:
         contact = paginator2.page(page2)
     except PageNotAnInteger:
         contact = paginator2.page(1)
     except EmptyPage:
         contact = paginator2.page(paginator2.num_pages)
     
     context['event'] = events
     context['posts'] = posts
     context['contact'] = contact
     context['homeadmin'] = 'active'
          
     return render(request,'news_events/admin.html',context)
 


def edit_post(request, slug):
     post = get_object_or_404(Post, slug=slug)
     if request.method == "POST":
         form = PostForm(request.POST,request.FILES, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
             return redirect(adminpath)
     else:
         form = PostForm(instance=post)  
     
     return render(request,'news_events/add_news.html',{'form':form})
 
def delete_new(request):
     
     if request.method == "GET" and request.GET.get('id'):
         id = request.GET.get('id')
         get_slug = Post.objects.get(id=id)
         get_slug.delete()
     
         return redirect(adminpath)


def add_news(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES)   
        if form.is_valid():
            form.save()
            form = PostForm ()
            return redirect(adminpath)
            
    context = {}

    context['form'] = form
    context['news_page'] = 'active'
    
    return render(request,"news_events/add_news.html",context)
 
 
 
 
 # Event
@login_required(login_url='/admin/login/')
def add_event(request):
     form = EventForm()
     if request.method == "POST":
         form = EventForm(request.POST , request.FILES)
         if form.is_valid():
             form.save()
             form = EventForm()
             return redirect(adminpath)
     context = {}
     context['form'] = form
     context['event_page'] = 'active'
 
     return render(request, "add_event.html",context)
     
def edit_event(request,pk):
     event = get_object_or_404(Event , pk=pk)
     if request.method == "POST":
         form = EventForm(request.POST,request.FILES,instance=event)
         if form.is_valid():
             form.save()
             return redirect(adminpath)
     else:
         form = EventForm(instance=event)
 
     return render(request,'add_event.html',{'form':form,'event':event})
 
def delete_event(request):
     if request.method == "GET" and request.GET.get('id'):
         id = request.GET.get('id')
         id_event = Event.objects.get(id=id)
         id_event.delete()
     
         return redirect(adminpath)
 
 
 #About
@login_required(login_url='/admin/login/')
def add_about(request):
     form = AboutForm()
     if request.method == 'POST':
         form = AboutForm(request.POST , request.FILES)   
         if form.is_valid():
             form.save()
             form = AboutForm ()
             return redirect(adminpath)
     
     context = {}
 
     context['form'] = form
     context['about_page'] = 'active'
     
     return render(request,"add_about.html",context)
def edit_about(request,pk):
     about = get_object_or_404(About, pk=pk)
     if request.method == "POST":
         form = AboutForm(request.Post, instance=about)
         if form.is_valid():
             form.save()
             return redirect(adminpath)
     else:
         form = AboutForm(instance=about)
     context = {}
     context['form'] = form
     
     return render(request,'add_about.html',context)
def about_data_page(request):
     form = AboutForm()
     aboutdata = About.objects.all()
     if request.method == 'POST':
         form = AboutForm(request.POST , request.FILES)   
         if form.is_valid():
             form.save()
             form = AboutForm ()
             return redirect(adminpath)
             
     context = {}
 
     context['about'] = aboutdata
     context['about_data_page'] = 'active'
    
     
     return render(request,"about_data_page.html",context)
 
 
 
 # Sign up
 

# function import plant data excel file
def upload_plant_data(request):
    try:
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                request.FILES['file'].save_book_to_database(
                    models=[specimen],
                    mapdicts=[
                        'biobank_id', 'family', 'genus', 'species',
                        'thai_vernacular_name', 'common_name',
                        'native_introduced', 'utilization'
                    ])
                return redirect('/Admin/upload_plant_data')
            else:
                return HttpResponseBadRequest()
        else:   
            form = UploadFileForm()
            return render(
                request, 'plants_databases/upload_plant_data.html', {
                    'form': form,
                    'title': 'Import excel data into database example',
                    'header': 'Please upload sample-data.xls:'
                })
    except Exception as e: 
        return HttpResponseServerError(e)
    finally:
        print('== end upload plant data ==')


# function specimen in state  collect
def specimen_collect(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
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
            return render(request, 'specimens/specimen_collect.html', content)
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function specimen_collect == ')


# function main logs
def logs(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'logs/logs.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function logs ==')


# function users profile 
def profile(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'profiles/profile.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end  function profile ==')


# function user notification
def notification(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'profiles/notification.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function notification ==')


# function users setting
def setting(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'profiles/setting.html', {})
    except:
        print('  render setting')


# function backup page list history backup
def backup(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'databases/backup.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end  function backup database ===')


#function backup database use for backup database mysql , 
def backup_database(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'databases/backup_database.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end function backup database ===')


# function backup web content for save file content 
def backup_web_content(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'databases/backup_web_content.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('=== end function log database ===')


# function create news
def create_news(request):
    try:
        if request.method == "POST":
             # receive POST
            name = request.POST.get('type_submit')
            if name == 'save':
                name_pic = request.FILES.getlist("name_pic")
                gallery_pic = request.FILES.getlist("gallery_pic")
                add_news = request.POST.get('title', '') # Post['tilte']
                add_detail = request.POST.get('detail', '')

                print("ok1")
                # param to fn (name_input, specimen_id, title_name, name_path_dir_in_media)
                image_new = rename_to_upload_photo(name_pic,None,'fw','photo_new_events')
                print("ok2")
                gallery_news = rename_to_upload_photo(gallery_pic,None,'fw','news_gallery')
                print("ok3")
                insert_row = new_event(
                    title = add_news,
                    detail = add_detail,
                    image_evevt = image_new,
                    image_gallery = gallery_news,
                    )
                print("ok4")
                insert_row.save()
            return redirect('/SmsBackEnd/manage_news_events/')
            # return render(request, 'news_events/create_news.html', {})
        else:
            return render(request, 'news_events/create_news.html', {})

    except:
        print('erro render add news ')


# function delete news 
@login_required()
def delete_new(request):
    try:
        if request.method == "POST":
            news_id = request.POST['news_id']

            new_delete = new_event.objects.filter(id = news_id).values()

            for i,v in enumerate(new_delete):
                new_delete[i]['image_evevt'] = v['image_evevt'][1:-1].replace("'","").split(', ')
            for i,v in enumerate(new_delete):
                new_delete[i]['image_gallery'] = v['image_gallery'][1:-1].replace("'","").split(', ')

            for n in new_delete:
                for im in n['image_evevt']:
                    deleteImage("media/photo_new_events/", im)

            for n in new_delete:
                for im in n['image_gallery']:
                    deleteImage("media/news_gallery/", im)
            
                   
            new_event.objects.filter(id = news_id).delete()        
            return redirect('/SmsBackEnd/manage_news_events/')
        else:

            return HttpResponse('Delete')

    except Exception as e:
        return HttpResponseServerError(e)


# function edit news
@login_required() 
def edit_news(request, id):
    try:
        if request.method == "POST":
            name = request.POST.get('type_submit')
            if name == 'update':
                edit_title = request.POST.get('title', '')
                edit_detail = request.POST.get('detail', '')
                name_pic = request.FILES.getlist('name_pic','')
                gallery_pic = request.FILES.getlist('gallery_pic','')
                # param to fn (name_input, specimen_id, title_name, name_path_dir_in_media)
            
                data_pic = rename_to_upload_photo(name_pic,None,'fw','photo_new_events')
                im_gallery = rename_to_upload_photo(gallery_pic,None,'fw','news_gallery')


                if data_pic == '':
                    meta_data = new_event.objects.filter(id=id).values('image_evevt')
                    for i in meta_data:
                        data_pic = i['image_evevt'][1:-1].replace("'","").split(', ')
                else:
                    meta_data = new_event.objects.filter(id=id).values('image_evevt')
                    for i in meta_data:
                        new_data_pic = i['image_evevt'][1:-1].replace("'","").split(', ')
                        data_pic.extend(new_data_pic)

                        # image_gallery
                if im_gallery == '':
                    meta_data = new_event.objects.filter(id=id).values('image_gallery')
                    for i in meta_data:
                        im_gallery = i['image_gallery'][1:-1].replace("'","").split(', ')
                else:
                    meta_data = new_event.objects.filter(id=id).values('image_gallery')
                    for i in meta_data:
                        new_im_gallery = i['image_gallery'][1:-1].replace("'","").split(', ')
                        im_gallery.extend(new_im_gallery)

                        # update to database
                new_event.objects.filter(id=id).update(
                    title=edit_title,
                    detail=edit_detail,
                    image_evevt=data_pic,
                    image_gallery=im_gallery,
                    )
                return redirect('/SmsBackEnd/edit_news/'+id+'/')
                # return redirect('/SmsBackEnd/manage_news_events/')

            elif name == 'deleteimage':
                
                news_id = request.POST['news_id']
                get_data = request.POST['get_data']              
               
                data = new_event.objects.filter(id = news_id).values('image_evevt')
                data_add = []
                for i  in data:
                    data_add = i['image_evevt'][1:-1].replace("'","").split(', ')
                new = data_add.pop(int(get_data)-1)

                # delete image from Dir
                deleteImage("media/photo_new_events/", new)

                data = []
                for i in data_add:
                    data.append(i)

                new_event.objects.filter(id = news_id).update(image_evevt = data)

                return redirect('/SmsBackEnd/edit_news/'+news_id+'/')
                # return redirect('/SmsBackEnd/manage_news_events/')

            else:
                 #name == 'deleteimagegallery':

                gallery_id = request.POST['gallery_id']
                gallery_data = request.POST['gallery_data'] 
                data_gallery = new_event.objects.filter(id = gallery_id).values('image_gallery')
                gallery_add = []
                for i  in data_gallery:
                    gallery_add = i['image_gallery'][1:-1].replace("'","").split(', ')
                new = gallery_add.pop(int(gallery_data)-1)

                # delete image from Dir
                deleteImage("media/news_gallery/", new)

                data_gallery = []
                for i in gallery_add:
                    data_gallery.append(i)
                
                new_event.objects.filter(id = gallery_id).update(image_gallery = data_gallery)
                
                return redirect('/SmsBackEnd/edit_news/'+gallery_id+'/')
                # return redirect('/SmsBackEnd/manage_news_events/')

        else:
            edit_news_to = new_event.objects.filter(id=id).values()
            
            for i,v in enumerate(edit_news_to):
                edit_news_to[i]['image_evevt'] = v['image_evevt'][1:-1].replace("'","").split(', ')

            # image_gallery
            for i,v in enumerate(edit_news_to):
                edit_news_to[i]['image_gallery'] = v['image_gallery'][1:-1].replace("'","").split(', ')

            content = {
                'edit_news': edit_news_to
            }
            return render(request, 'news_events/edit_news.html', content)

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function edit news ==')


# function Views news
@login_required() 
def view_news(request, id):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            view_news_to = new_event.objects.filter(id=id).values()
            
            for i,v in enumerate(view_news_to):
                # print(i['image_evevt'][1:-1].replace("'",""))
                view_news_to[i]['image_evevt'] = v['image_evevt'][1:-1].replace("'","").split(', ')
                # print(news[i]['image_evevt']+'<<<<<<<<<<<<<<')

            for i,v in enumerate(view_news_to):
                # print(i['image_evevt'][1:-1].replace("'",""))
                view_news_to[i]['image_gallery'] = v['image_gallery'][1:-1].replace("'","").split(', ')
                # print(news[i]['image_evevt']+'<<<<<<<<<<<<<<')
           
            content = {
                'view_to': view_news_to
            }
            return render(request, 'news_events/view_news.html', content)

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function edit news ==')


# function manage news
@login_required()
def manage_news_events(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SmsBackEnd_new_event ORDER BY SmsBackEnd_new_event.id DESC")
    news = dictfetchall(cursor)
    cursor.close()
        
    for i,v in enumerate(news):
        news[i]['image_evevt'] = v['image_evevt'][1:-1].replace("'","").split(', ')

    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            
            context = {
                
                'new': news
                }
            return render(request, 'news_events/manage_news_events.html',context)

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end  function manage news events ==')


#Function load Events
@login_required() 
def load_events(request):
    try:
            data = []
            events_load = events_biobank.objects.filter().order_by('id').values()
            for i in events_load:
                # print({'id': i['id'], 'title': i['events_title'],'start': "",'end': ""})
                data.append({'id': i['id'], 'title': i['events_title'],'start': i['start_event'],'end': i['end_event']})
            # return JsonResponse(list(events_biobank.objects.all().values()), safe=False)
            # return HttpResponse(json.dumps(events_load))
            return JsonResponse(data, safe=False)
            # return render(request, 'news_events/load_events.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end  function add events ==')

#Function insert Events
@login_required() 
def insert_events(request):
    try:
        if request.method == "POST":
            title = request.POST.get('title', '')
            start = request.POST.get('start', '')
            end = request.POST.get('end', '')
            # '2019-06-17 00:00:00', '2019-06-17 00:00:00'
            nsert_event = events_biobank(
                    events_title = title,
                    start_event = start,
                    end_event = end,
                    )
            nsert_event.save()
            
            return render(request, 'news_events/views_events.html', {})
        else:
            return render(request, 'news_events/views_events.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('==end function changecontent==')


#Function Update Events
@login_required() 
def update_events(request):
    try:
        if request.method == "POST":
            id_events = request.POST.get('id', '')
            title = request.POST.get('title', '')
            start = request.POST.get('start', '')
            end = request.POST.get('end', '')

            # '2019-06-17 00:00:00', '2019-06-17 00:00:00'
            events_biobank.objects.filter(id=id_events).update(
                id = id_events,
                events_title = title,
                start_event = start,
                end_event =end,
                )
          
            return render(request, 'news_events/views_events.html', {})
        else:
            return render(request, 'news_events/views_events.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('==end function changecontent==')


#Function Delete Events
@login_required() 
def delete_events(request):
    try:
        if request.method == "POST":
            id_events = request.POST.get('id', '')
            events_biobank.objects.filter(id = id_events).delete()    
            return render(request, 'news_events/views_events.html', {})
        else:
            return render(request, 'news_events/views_events.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('==end function changecontent==')


#Function views Events
@login_required() 
def views_events(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'news_events/views_events.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('==end function changecontent==')


def change_content(request):
    try:
        
        if request.method == "POST":
            name = request.POST.get('type_submit')
            if name == 'HomePage':
                title = request.POST.get('title_HomePage', '')
                contents = request.POST.get('contents_HomePage', '')
                image_c = request.FILES.getlist('image_HomePage','')
                
                # param to fn (name_input, specimen_id, title_name, name_path_dir_in_media)
                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 500
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    im2.save("media/image_contents/"+im) 

                insert_row = change_contents(
                    id = 1,
                    title = title,
                    contents = contents,
                    image_contents = image_new,
                    )
                insert_row.save()
            elif name == 'AboutPage':
                title = request.POST.get('title_AboutPage', '')
                contents = request.POST.get('contents_AboutPage', '')
                image_c = request.FILES.getlist('image_AboutPage','')
                # param to fn (name_input, specimen_id, title_name, name_path_dir_in_media)
                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 250
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    im2.save("media/image_contents/"+im) 

                insert_row = change_contents(
                    id = 2,
                    title = title,
                    contents = contents,
                    image_contents = image_new,
                    )
                insert_row.save()
            elif name == 'NewsEvents':
                title = request.POST.get('title_NewsEvents', '')
                contents = request.POST.get('contents_NewsEvents', '')
                image_c = request.FILES.getlist('image_NewsEvents','')
                
                # param to fn (name_input, specimen_id, title_name, name_path_dir_in_media)
                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 250
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    im2.save("media/image_contents/"+im) 

                insert_row = change_contents(
                    id = 3,
                    title = title,
                    contents = contents,
                    image_contents = image_new,
                    )
                insert_row.save()
            elif name == 'Contact':
                title = request.POST.get('title_Contact', '')
                contents = request.POST.get('contents_Contact', '')
                image_c = request.FILES.getlist('image_Contact','')
               
                # param to fn (name_input, specimen_id, title_name, name_path_dir_in_media)
                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 250
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    im2.save("media/image_contents/"+im) 

                insert_row = change_contents(
                    id = 4,
                    title = title,
                    contents = contents,
                    image_contents = image_new,
                    )
                insert_row.save()
            elif name == 'up_HomePage':
                title = request.POST.get('title_HomePage', '')
                contents = request.POST.get('contents_HomePage', '')
                image_c = request.FILES.getlist('image_HomePage','')

                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 500
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    deleteImage("media/image_contents/", im)
                    im2.save("media/image_contents/"+im) 

                if image_new == '':
                    meta_data = change_contents.objects.filter(id=1).values('image_contents')
                    for i,v in enumerate(meta_data):
                        meta_data[i]['image_contents'] = v['image_contents'].replace(", ''","")
                        meta_data[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                        image_new =  meta_data[i]['image_contents']
                      
                else:
                    meta_data = change_contents.objects.filter(id=1).values('image_contents')
                    for i,v in enumerate(meta_data):
                        meta_data[i]['image_contents'] = v['image_contents'].replace(", '']","]")
                        meta_data[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                        new_data_pic = meta_data[i]['image_contents']
                        image_new.extend(new_data_pic)
            
                change_contents.objects.filter(id = 1).update(
                    title = title,
                    contents=contents,
                    image_contents = image_new,
                )
            elif name == 'up_AboutPage':
                title = request.POST.get('title_AboutPage', '')
                contents = request.POST.get('contents_AboutPage', '')
                image_c = request.FILES.getlist('image_AboutPage','')

                change_homepage = change_contents.objects.filter(id = 2).values()
                for i,v in enumerate(change_homepage):
                    change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                    if image_c == '':
                        pass
                    else:
                        for im in change_homepage:
                            for it in im['image_contents']:
                                deleteImage("media/image_contents/", it)

                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 250
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    # deleteImage("media/image_contents/", im)
                    im2.save("media/image_contents/"+im) 


                def check_img(col_db,check):
                    if check == '':
                        meta_data = change_contents.objects.filter(id=2).values(col_db)
                        for i in meta_data:
                            check = i[col_db][1:-1].replace("'","").split(', ')                 
                    if check == ['']:
                        check = ''
                    return check
                
                image_new = check_img('image_contents',image_new)

                change_contents.objects.filter(id = 2).update(
                    title = title,
                    contents=contents,
                    image_contents = image_new,
                )
            elif name == 'up_NewsEvents':
                title = request.POST.get('title_NewsEvents', '')
                contents = request.POST.get('contents_NewsEvents', '')
                image_c = request.FILES.getlist('image_NewsEvents','')

                change_homepage = change_contents.objects.filter(id = 3).values()
                for i,v in enumerate(change_homepage):
                    change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                if image_c == '':
                    pass
                else:
                    for im in change_homepage:
                        for it in im['image_contents']:
                            deleteImage("media/image_contents/", it)


                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 250
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    # deleteImage("media/image_contents/", im)
                    im2.save("media/image_contents/"+im) 


                def check_img(col_db,check):
                    if check == '':
                        meta_data = change_contents.objects.filter(id=3).values(col_db)
                        for i in meta_data:
                            check = i[col_db][1:-1].replace("'","").split(', ')                 
                    if check == ['']:
                        check = ''
                    return check
                
                image_new = check_img('image_contents',image_new)

                change_contents.objects.filter(id = 3).update(
                    title = title,
                    contents=contents,
                    image_contents = image_new,
                )
            elif name == 'up_Contact':
                title = request.POST.get('title_Contact', '')
                contents = request.POST.get('contents_Contact', '')
                image_c = request.FILES.getlist('image_Contact','')

                change_homepage = change_contents.objects.filter(id = 4).values()
                for i,v in enumerate(change_homepage):
                    change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                if image_c == '':
                    pass
                else:
                    for im in change_homepage:
                        for it in im['image_contents']:
                            deleteImage("media/image_contents/", it)


                image_new = rename_to_upload_photo(image_c,None,'fw','image_contents')
                for im in image_new:
                    im1 = Image.open('media/image_contents/'+im)
                    width = 1500
                    height = 250
                    im2 = im1.resize((width, height), Image.ANTIALIAS)      # use nearest neighbour
                    # deleteImage("media/image_contents/", im)
                    im2.save("media/image_contents/"+im) 


                def check_img(col_db,check):
                    if check == '':
                        meta_data = change_contents.objects.filter(id=4).values(col_db)
                        for i in meta_data:
                            check = i[col_db][1:-1].replace("'","").split(', ')                 
                    if check == ['']:
                        check = ''
                    return check
                
                image_new = check_img('image_contents',image_new)

                change_contents.objects.filter(id = 4).update(
                    title = title,
                    contents=contents,
                    image_contents = image_new,
                )
            elif name == 'clear_HomePage':
                contents_de = change_contents.objects.filter(id = 1).values()
                for i,v in enumerate(contents_de):
                    contents_de[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')

                for n in contents_de:
                    for i in n['image_contents'] :
                        deleteImage("media/image_contents/", i)

                change_contents.objects.filter(id = 1).update(
                    image_contents = '',
                )

            return redirect('/SmsBackEnd/change_content/')
            # return HttpResponseBadRequest()
        else:
            change_do = change_contents.objects.filter().values()
            
            # for i,v in enumerate(change_homepage):
            #     change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
            change_valuein = 0
            change_value = 0
            if len(change_do) == 0:
                change_value = 0

            elif len(change_do) > 0:
                change_value = 1
                if len(change_do) == 1:
                    change_valuein = 1
                    # Home Page
                    change_homepage = change_contents.objects.filter(id = 1).values()
                    for i,v in enumerate(change_homepage):
                        change_homepage[i]['image_contents'] = v['image_contents'].replace(", '']","]")
                        change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                        

                    content = {
                        'change_homepage': change_homepage,
                        'change_value' : change_value,
                        'change_valuein' : change_valuein 
                    }                        
                elif len(change_do) == 2:
                    change_valuein = 2
                    # Home Page
                    change_homepage = change_contents.objects.filter(id = 1).values()
                    for i,v in enumerate(change_homepage):
                        change_homepage[i]['image_contents'] = v['image_contents'].replace(", '']","]")
                        change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
           
                    # About Page
                    change_aboutpage = change_contents.objects.filter(id = 2).values()
                    for i,v in enumerate(change_aboutpage):
                        change_aboutpage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                   
                    content = {
                        'change_homepage': change_homepage,
                        'change_aboutpage' : change_aboutpage,
                        'change_value' : change_value,
                        'change_valuein' : change_valuein 
                    } 
                elif len(change_do) == 3:
                    change_valuein = 3
                    # Home Page
                    change_homepage = change_contents.objects.filter(id = 1).values()
                    for i,v in enumerate(change_homepage):
                        change_homepage[i]['image_contents'] = v['image_contents'].replace(", '']","]")
                        change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                    
                    # About Page
                    change_aboutpage = change_contents.objects.filter(id = 2).values()
                    for i,v in enumerate(change_aboutpage):
                        change_aboutpage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                   
                    # News and Events Page
                    change_newsevent = change_contents.objects.filter(id = 3).values()
                    for i,v in enumerate(change_newsevent):
                        change_newsevent[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                    
                    content = {
                        'change_homepage': change_homepage,
                        'change_aboutpage' : change_aboutpage,
                        'change_newe' : change_newsevent,
                        'change_value' : change_value,
                        'change_valuein' : change_valuein 
                    } 
                elif len(change_do) == 4:
                    change_valuein = 4
                    # Home Page
                    change_homepage = change_contents.objects.filter(id = 1).values()

                    for i,v in enumerate(change_homepage):
                        # change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                        change_homepage[i]['image_contents'] = v['image_contents'].replace(", '']","]")
                        change_homepage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')

                    # About Page
                    change_aboutpage = change_contents.objects.filter(id = 2).values()
                    for i,v in enumerate(change_aboutpage):
                        change_aboutpage[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')

                    # News and Events Page
                    change_newsevent = change_contents.objects.filter(id = 3).values()
                    for i,v in enumerate(change_newsevent):
                        change_newsevent[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                    
                    # Contact Page
                    change_contact = change_contents.objects.filter(id = 4).values()
                    for i,v in enumerate(change_contact):
                        change_contact[i]['image_contents'] = v['image_contents'][1:-1].replace("'","").split(', ')
                    
                    content = {
                        'change_homepage': change_homepage,
                        'change_aboutpage' : change_aboutpage,
                        'change_newe' : change_newsevent,
                        'change_contact' : change_contact,
                        'change_value' : change_value,
                        'change_valuein' : change_valuein 
                    } 
                else:
                    pass
           
            if change_value == 0:
                content_value = {
                    'change_value' : change_value
                }
                return render(request, 'contents/change_content.html', content_value)
            else:
                return render(request, 'contents/change_content.html', content)
                    

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('==end function changecontent==')


def list_job(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'jobs/list_job.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function list job ==')


def edit_job(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'jobs/edit_job.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function edit job ==')


def create_job(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'jobs/create_job.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print(' == end function create job ==')


def list_queries(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'queries/list_queries.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function list queries==')


def edit_queries(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'queries/edit_queries.html', {})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end function edit queies')


def create_queries(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            return render(request, 'queries/create_queries.html', {})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end funtion render create queries ==')


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        

class Transfer_order(View):
    def get(self, request, *args, **kwargs):
        param = self.request.GET.get('date',None)
        if param:            
            count_seed_lab = print_order.objects.filter(lab='seed_lab',doc_number=param).count()
            count_herbarium_lab = print_order.objects.filter(lab='herbarium_lab',doc_number=param).count()
            count_molecular_lab = print_order.objects.filter(lab='molecular_lab',doc_number=param).count()
            count_tissue_lab = print_order.objects.filter(lab='tissue_lab',doc_number=param).count()
            # 
            tb_seed_lab = print_order.objects.filter(lab='seed_lab',doc_number=param).values_list('specimen_id',flat=True)
            tb_seed_lab = specimen.objects.filter(id__in=list(tb_seed_lab)).values()
            # 
            tb_herbarium_lab = print_order.objects.filter(lab='herbarium_lab',doc_number=param).values_list('specimen_id',flat=True)
            tb_herbarium_lab = specimen.objects.filter(id__in=list(tb_herbarium_lab)).values()
            # 
            tb_molecular_lab = print_order.objects.filter(lab='molecular_lab',doc_number=param).values_list('specimen_id',flat=True)
            tb_molecular_lab = specimen.objects.filter(id__in=list(tb_molecular_lab)).values()
            # 
            tb_tissue_lab = print_order.objects.filter(lab='tissue_lab',doc_number=param).values_list('specimen_id',flat=True)
            tb_tissue_lab = specimen.objects.filter(id__in=list(tb_tissue_lab)).values()
            param = param
        else:    
            count_seed_lab = print_order.objects.filter(lab='seed_lab',status='Waiting').count()
            count_herbarium_lab = print_order.objects.filter(lab='herbarium_lab',status='Waiting').count()
            count_molecular_lab = print_order.objects.filter(lab='molecular_lab',status='Waiting').count()
            count_tissue_lab = print_order.objects.filter(lab='tissue_lab',status='Waiting').count()
            # 
            tb_seed_lab = print_order.objects.filter(lab='seed_lab',status='Waiting').values_list('specimen_id',flat=True)
            tb_seed_lab = specimen.objects.filter(id__in=list(tb_seed_lab)).values()
            # 
            tb_herbarium_lab = print_order.objects.filter(lab='herbarium_lab',status='Waiting').values_list('specimen_id',flat=True)
            tb_herbarium_lab = specimen.objects.filter(id__in=list(tb_herbarium_lab)).values()
            # 
            tb_molecular_lab = print_order.objects.filter(lab='molecular_lab',status='Waiting').values_list('specimen_id',flat=True)
            tb_molecular_lab = specimen.objects.filter(id__in=list(tb_molecular_lab)).values()
            # 
            tb_tissue_lab = print_order.objects.filter(lab='tissue_lab',status='Waiting').values_list('specimen_id',flat=True)
            tb_tissue_lab = specimen.objects.filter(id__in=list(tb_tissue_lab)).values()
            # 
            sysdate = datetime.datetime.now().strftime("%Y-%m-%d")
            sys_date = datetime.datetime.now().strftime("%Y_%m_%d")
            last_times = print_order.objects.aggregate(Max('id'))
            last_times = encode(last_times['id__max'])
            print_order.objects.filter(status='Waiting').update(status='Approved',date_print=sysdate,doc_number=sys_date+'_'+last_times)
            param = sys_date+'_'+last_times

        data = {
            'count_seed_lab':count_seed_lab,
            'count_herbarium_lab':count_herbarium_lab,
            'count_molecular_lab':count_molecular_lab,
            'count_tissue_lab':count_tissue_lab,
            'today': datetime.date.today(),
            'tb_seed_lab': tb_seed_lab,
            'tb_herbarium_lab': tb_herbarium_lab,
            'tb_molecular_lab': tb_molecular_lab,
            'tb_tissue_lab': tb_tissue_lab,
            'doc_number':param
        }


        pdf = render_to_pdf('send_specimen/pdf_transfer_order.html', data)
        return HttpResponse(pdf, content_type='application/pdf')