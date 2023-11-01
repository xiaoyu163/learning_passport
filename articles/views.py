from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from django.contrib import messages

import os
import pandas as pd
import openpyxl
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from events.models import Events, Event_Participants, Event_Form
from users.models import Organisation,Student,User,OrgComittee
from .models import Article
from datetime import datetime

# Create your views here.
def eventComFormView (request):
    event_list = Events.objects.all()
    context = {
        "events": event_list,
    }
    if request.method == 'POST':
        event = Events.objects.get(id=request.POST['event_id'])
        if 'submit' in request.POST:         
            if not Event_Form.objects.filter(event=event).exists():             
                form = Event_Form()
                student = Student.objects.get(user_id=request.user.id)                
                form.event = event
                form.submit_by = student
                form.save()            
                matrics = request.POST.getlist('matric[]')
                positions = request.POST.getlist('position[]')           
                for i in range (len(matrics)):
                    student = Student.objects.get(matric_no=matrics[i].lower())
                    if Event_Participants.objects.filter(event=event, student=student).exists():
                        event_par = Event_Participants.objects.get(event=event, student=student)
                    else:
                        event_par = Event_Participants()
                        event_par.event = event
                        event_par.student = student
                    event_par.event_form = form
                    event_par.position = positions[i]
                    print(event_par)
                    event_par.save()                
            else:
                form = Event_Form.objects.get(event=event)
                messages.error(request, "Event Comittee was submitted. Please edit the previous submission.")
                

        
        return redirect("submit-event")
    return render(request, "event_com_form.html", context)

def submitEventView (request):
  
 
    student = Student.objects.get(user=request.user.id)
    forms = Event_Form.objects.filter(submit_by=student)
   
    context = {
        "page_name": "Upload Event Documents",
        "forms": forms    
    
    }


    return render (request, "upload_event.html", context)

def editEventComView (request, form_id):
    form = Event_Form.objects.get(id=form_id)
    event_name = form.event.e_name
    coms = Event_Participants.objects.filter(event_form=form)
    students = list()
    for com in coms:
        students.append(com.student)
    coms_students = zip(coms,students)
    print(coms_students)
    context = {
        "page_name": "Edit Event Documents",
        "coms_students": coms_students,
        "event_name": event_name,
    
    }

    if request.method == 'POST':
        matrics = request.POST.getlist('matric[]')
        positions = request.POST.getlist('position[]')    
        for com in coms:
            if com.student.matric_no not in matrics:
                com.delete()       
        for i in range (len(matrics)):
            student = Student.objects.get(matric_no=matrics[i].lower())
            if Event_Participants.objects.filter(event=form.event, student=student).exists():
                event_par = Event_Participants.objects.get(event=form.event, student=student)
            else:
                event_par = Event_Participants()
                event_par.event = form.event
                event_par.student = student
                event_par.event_form = form
            event_par.position = positions[i]
            print(event_par)
            form.save()
            event_par.save()  
        return redirect (request.get_full_path())  
        
    return render (request, "event_com_form.html", context)
def submitOrgView (request):
    student = Student.objects.get(user=request.user.id)
    orgs = Organisation.objects.filter(file_by=student)

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
                return redirect("submit-org")
                
    return render (request, "upload_org.html", context)

def submitArticleView (request):
    student = Student.objects.get(user=request.user.id)
    arts = Article.objects.filter(file_by=student)

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
                return redirect("submit-article")
        
   
    return render(request, "upload_article.html", context)

def download_excel(request, template_name):
    file_path = os.path.join(settings.BASE_DIR, 'media/template', template_name+'.xlsx')
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response

@login_required
@role_required(['SUPER ADMIN','ADMIN'])
def verEventView (request):
    pending_events = Events.objects.exclude(file__exact='').exclude(status__in=[0, 1])
    approved_events= Events.objects.filter(status=1)
    rejected_events = Events.objects.exclude(file__exact='').filter(status=0)
    pending_data = {
    'events': pending_events,  # Replace pending_orgs with your data
    'pending': True,
    }
    approved_data = {
    'events': approved_events,  # Replace pending_orgs with your data
    'pending': False,
    }
    rejected_data = {
    'events': rejected_events,  # Replace pending_orgs with your data
    'pending': False,
    "rejected":True,
    }
    context = {
        "page_name": "Verify Event Comittee",
        "pending_data": pending_data,
        "approved_data": approved_data,
        "rejected_data": rejected_data,
     
    }

    if request.POST:
        event = Events.objects.get(id=request.POST['event'])
        if 'reject' in request.POST:
            event.status = 0
            event.save()
        else:
            event.status = 1
            base_dir = str(settings.BASE_DIR).replace("\\","/")
            file_url = event.file.url
            file_path = base_dir + file_url            

            com_df = pd.read_excel(file_path,  names=["position","name","matric"])
            for com in com_df.iterrows():
                student = Student.objects.get(matric_no=com[1]['matric'].lower())
                if Event_Participants.objects.filter(event=event, student=student).exists():
                    event_par = Event_Participants.objects.get(event=event, student=student)
                else:
                    event_par = Event_Participants()
                    event_par.event = event
                    event_par.student = student
                event_par.position = com[1]['position']
                event_par.save()
                
            os.remove(file_path)
            event.file = None
            event.save()

        return redirect ("verify-event")

    return render(request, "verify_event.html", context)

@login_required
@role_required(['SUPER ADMIN','ADMIN'])
def verOrgView (request):
    pending_orgs = Organisation.objects.exclude(file__exact='').exclude(status__in=[0, 1])
    approved_orgs = Organisation.objects.filter(status=1)
    rejected_orgs = Organisation.objects.exclude(file__exact='').filter(status=0)
    pending_data = {
    'orgs': pending_orgs,  # Replace pending_orgs with your data
    'pending': True,
    }
    approved_data = {
    'orgs': approved_orgs,  # Replace pending_orgs with your data
    'pending': False,
    }
    rejected_data = {
    'orgs': rejected_orgs,  # Replace pending_orgs with your data
    'pending': False,
    "rejected": True,
    }
    context = {
        "page_name": "Verify Organisation Comittee",
        "pending_data": pending_data,
        "approved_data": approved_data,
        "rejected_data": rejected_data,
     
    }

    if request.POST:
        org = Organisation.objects.get(id=request.POST['org'])
        if 'reject' in request.POST:
            org.status = 0
            org.save()
        else:
            org.status = 1
            base_dir = str(settings.BASE_DIR).replace("\\","/")
            file_url = org.file.url
            file_path = base_dir + file_url
            com_df = pd.read_excel(file_path,  names=["position","name","matric"])
            for com in com_df.iterrows():
                student = Student.objects.get(matric_no=com[1]['matric'].lower() )
                if OrgComittee.objects.filter(org=org, student=student).exists():
                    org_com = OrgComittee.objects.get(org=org, student=student)
                else:
                    org_com = OrgComittee()
                    org_com.org = org
                    org_com.student = student
                org_com.position = com[1]['position']
                org_com.save()
            os.remove(file_path)
            org.file = None
            org.save()
        return redirect ("verify-org")

    return render(request, "verify_org.html", context)

@login_required
@role_required(['SUPER ADMIN','ADMIN'])
def verArtView (request):
    pending_arts = Article.objects.exclude(file__exact='').exclude(status__in=[0, 1])
    approved_arts= Article.objects.filter(status=1)
    rejected_arts = Article.objects.exclude(file__exact='').filter(status=0)
    pending_data = {
    'arts': pending_arts,  
    'pending': True,
    }
    approved_data = {
    'arts': approved_arts,  
    'pending': False,
    }
    rejected_data = {
    'arts': rejected_arts,  
    'pending': False,
    'rejected': True,
    }
    context = {
        "page_name": "Verify Article",
        "pending_data": pending_data,
        "approved_data": approved_data,
        "rejected_data": rejected_data,
     
    }

    if request.POST:
        art = Article.objects.get(id=request.POST['art'])
        if 'reject' in request.POST:
            art.status = 0
            art.save()
        else:
            art.status = 1
            base_dir = str(settings.BASE_DIR).replace("\\","/")
            file_url = art.file.url
            file_path = base_dir + file_url
            os.remove(file_path)
            art.file = None
            art.save()
        return redirect ("verify-article")

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
