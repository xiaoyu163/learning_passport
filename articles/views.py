from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from django.contrib import messages

import os
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from events.models import Events, Event_Participants
from users.models import Organisation,Student,User
from .models import Article
from datetime import datetime

# Create your views here.
def uploadEventView (request):
    option_obj = Events.type.field.choices
    event_list = Events.objects.all()
    student = Student.objects.get(user=request.user.id)
    events = Events.objects.filter(file_by=student).exclude(file__exact='')
   
    context = {
        "page_name": "Upload Event Documents",
        "option_obj": option_obj,
        "event_list": event_list,
        "events": events,
    }

    if request.POST:
        if 'event_submit' in request.POST:
            event = Events.objects.get(id=request.POST['event_id'])
            if not event.file:
                event.file = request.FILES['event_file']
                event.file_by = Student.objects.get(user=request.user.id)
                event.save()
            else:
                messages.error(request, "Event comittee list was uploaded.")
                return redirect("upload-event")
    
    return render (request, "upload_event.html", context)

def uploadOrgView (request):
    student = Student.objects.get(user=request.user.id)
    orgs = Organisation.objects.filter(file_by=student).exclude(file__exact='')

    context = {
        "page_name": "Upload Organisation Files",
        "orgs": orgs
       
    }

    if request.POST:
        if 'org_submit' in request.POST:
            if not Organisation.objects.filter(name=request.POST['org_name'], year=request.POST['org_year']).exists():
                org = Organisation()            
                org.name = request.POST['org_name']
                org.year = request.POST['org_year']
                org.internal = request.POST['org_internal']
                org.file = request.FILES['org_file']
                org.file_by = Student.objects.get(user=request.user.id)
                org.save()

            else:
                messages.error(request, "Organisation comittee list was uploaded.")
                return redirect("upload-org")
                
    return render (request, "upload_org.html", context)

def uploadArticleView (request):
    student = Student.objects.get(user=request.user.id)
    arts = Article.objects.filter(file_by=student).exclude(file__exact='')

    context = {
        "page_name": "Upload Articles",
        "arts": arts
    }
    if request.POST:       

        if 'art_submit' in request.POST:
            student = Student.objects.get(user_id = request.user.id)
            if not Article.objects.filter(title=request.POST['art_title']).exists():

                article = Article()
                article.title = request.POST['art_title']
                article.year = request.POST['art_year']
                article.type = request.POST['art_type']
                article.platform = request.POST['art_platform']
                article.comp = request.POST['art_comp']
                article.award = request.POST['art_awd']
                article.file = request.FILES['art_file']
                article.file_by = student
                article.save()
            else:
                messages.error(request, "Article was uploaded.")
                return redirect("upload-article")
        
   
    return render(request, "upload_article.html", context)

def download_excel(request, template_name):
    file_path = os.path.join(settings.BASE_DIR, 'media/template', template_name+'.xlsx')
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response

@login_required
@role_required(['SUPER ADMIN','ADMIN'])
def verEventView (request):
    events = Events.objects.exclude(file__exact='')
    context = {
        "page_name": "Verify Event Comittee",
        "events": events,
     
    }

    if request.POST:
        event = Events.objects.get(id=request.POST['event'])
        if 'reject' in request.POST:
            event.status = 0
            event.save()
        else:
            event.status = 1
            event.save()

    return render(request, "verify_event.html", context)

@login_required
@role_required(['SUPER ADMIN','ADMIN'])
def verOrgView (request):
    orgs = Organisation.objects.exclude(file__exact='')

    context = {
        "page_name": "Verify Organisation Comittee",
        "orgs": orgs,
     
    }

    if request.POST:
        org = Organisation.objects.get(id=request.POST['org'])
        if 'reject' in request.POST:
            org.status = 0
            org.save()
        else:
            org.status = 1
            org.save()

    return render(request, "verify_org.html", context)

@login_required
@role_required(['SUPER ADMIN','ADMIN'])
def verArtView (request):
    articles = Article.objects.exclude(file__exact='')
    print(articles)
    context = {
        "page_name": "Verify Articles",
        "articles": articles,
     
    }

    if request.POST:
        art = Article.objects.get(id=request.POST['art'])
        if 'reject' in request.POST:
            art.status = 0
            art.save()
        else:
            art.status = 1
            art.save()

    return render(request, "verify_art.html", context)

def statusView (request):
    student = Student.objects.get(user=request.user.id)
    events = Events.objects.filter(file_by=student).exclude(file__exact='')
    orgs = Organisation.objects.filter(file_by=student).exclude(file__exact='')
    arts = Article.objects.filter(file_by=student).exclude(file__exact='')
    context = {
        "page_name": "Upload Status",
        "events": events,
        "orgs": orgs,
        "arts":arts
    }
    return render (request, "status.html", context)
