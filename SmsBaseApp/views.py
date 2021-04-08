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
from .models import Post , Event , About 
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger       
from django.core import serializers
from django.views import generic
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from SmsBackEnd.form import ContactForm


# Home page
@login_required()
def index(request):
    c = connection.cursor()  
    # get list of all project
    try:
        user_session = request.session.get('user_session')
        if request.user is not None:
            context = {     
                'user_session':user_session
            }
            return render(request, 'home_page.html', context)
        else:
            return redirect('/Users/login/')
    finally:
        c.close()
        print('error')


# About page
@login_required()
def about(request):
    try:
        context = {
                }          
        return render(request, 'about_page.html', context)
    finally:
        print('error render about_page')


def contact(request):
     context = {"contact_page": "active"}
     form = ContactForm(request.POST or None)
     if request.method == "POST":
         pdict = request.POST.copy()
         form = ContactForm(pdict)
         
         if form.is_valid():
             subject = form.cleaned_data.get("subject")
             message = form.cleaned_data.get("message")
             from_email = form.cleaned_data.get("from_email")
             email = EmailMessage(
                 subject,
                 message, 
                 from_email,
                 to=['s59122201036@ssru.ac.th'],
                 )
             email.send()
             form.save()
             form = ContactForm()
 
     context['form'] = form
     queryset = Post.objects.filter(status=1).order_by('-created_on')
     # context['post_list'] = queryset
     paginator = Paginator(queryset, 5)
     page = request.GET.get('page')
     try:
         posts = paginator.page(page)
     except PageNotAnInteger:
         posts = paginator.page(1)
     except EmptyPage:
         posts = paginator.page(paginator.num_pages)
     context['posts'] = posts
     
     return render(request,'contact_page.html',context)



# News event page
def news_event(request):
     context={"News_event_page":"active"}
     most_view = Post.objects.filter(status=1).annotate(view_count=Max('visit_num')).order_by('-view_count')[:1]
     queryset = Post.objects.filter(status=1  ).order_by('-created_on')
     
     paginator = Paginator(queryset, 5)
     page = request.GET.get('page')
     try:
         posts = paginator.page(page)
     except PageNotAnInteger:
         posts = paginator.page(1)
     except EmptyPage:
         posts = paginator.page(paginator.num_pages)
 
     # fullcalendar events data
     events = eval(serializers.serialize("json",Event.objects.all()))
     events = list(map(lambda x:x['fields'],events))
 
     query = Event.objects.all()
     paginator1 = Paginator(query,5)
     page1 = request.GET.get('page1')
     try:
         event = paginator1.page(page1)
     except PageNotAnInteger:
         event = paginator1.page(1)
     except EmptyPage:
         event = paginator1.page(paginator1.num_pages)
 
     context['event'] = event
     context['events'] = events
     context['posts'] = posts
     context['most_view'] = most_view
     return render(request,'news_event_page.html',context)
 

def news_full_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.visit_num = F('visit_num') + 1
    post.save(update_fields=['visit_num'])
    task = Post.objects.filter(status=1).order_by('-created_on')[0:3]
    context = {}
    context['task'] = task
    context['post'] = post
    return render(request, 'news_full_detail.html',context)


class EventDetail(generic.DetailView):
     model = Event
     template_name = 'event_detail.html'
 
     def get_context_data(self, **kwargs):
         context = super(EventDetail, self).get_context_data(**kwargs)
         context['tasks'] = Event.objects.all()[0:3]
         return context
 
 

def news_info_page(req):
     context={"news_info_page":"active"}
     queryset = Post.objects.filter(status=1).order_by('-created_on')
     # context['post_list'] = queryset
     paginator = Paginator(queryset, 5)
     page = req.GET.get('page')
     try:
         posts = paginator.page(page)
     except PageNotAnInteger:
         posts = paginator.page(1)
     except EmptyPage:
         posts = paginator.page(paginator.num_pages)
     context['posts'] = posts
     return render(req,'news_info_page.html',context)
 
 
 
class Get_news_List(APIView):
     def get(self, request):
         news = Post.objects.filter(status=1).order_by('-created_on')[0:2]
         serialized_news =  PostSerializer(news, many=True)
         return Response(serialized_news.data)
 
 






