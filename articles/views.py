from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from django.contrib import messages

import os
import re
from django.db.models import Q
import pandas as pd
import openpyxl
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from events.models import Events, Event_Participants, OtherComp
from users.models import Organisation, Student, User, OrgComittee
from .models import Article
from datetime import datetime
from django.http import JsonResponse

# Create your views here.


def submitEventView(request):
    base_dir = str(settings.BASE_DIR).replace("\\", "/")
    option_obj = Events.type.field.choices
    events_in = Events.objects.filter(internal=1).exclude(status=1).exclude(file__isnull=False)
    events_ex = Events.objects.filter(internal=0).exclude(status=1)

    student = Student.objects.get(user=request.user.id)
    events = Events.objects.filter(file_by=student).exclude(file__exact='').exclude(file__exact=None)
    event_list = list()
    for event in events:
        event_list.append(event)
   
    event_pars = Event_Participants.objects.exclude(file__exact='').exclude(file__exact=None).filter(student=student)

    context = {
        "page_name": "Upload Event Documents",
        "option_obj": option_obj,
        "events_in": events_in,
        "events_ex": events_ex,
        "events": events,
        "event_pars": event_pars,
    }

    if request.POST:
        print(request.POST)
        if 'internal' in request.POST:
            if 'event_id' in request.POST and not request.POST['event_id'] == 'other':
                event = Events.objects.get(id=request.POST['event_id'])
                event.file = request.FILES['event_file']
                event.filename = request.FILES['event_file']
                event.file_by = Student.objects.get(user=request.user.id)
                event.save()
        
            else:
                event = Events()
                event.e_name = request.POST['otherOption']
                event.start = datetime.strptime(
                    request.POST['otherOptionDate'], '%Y-%m-%dT%H:%M')
                event.year = request.POST['otherOptionDate'][0:4]
                if 'otherOptionSpeaker' in request.POST:
                    event.speaker = request.POST['otherOptionSpeaker']
                event.type = request.POST['otherOptionType']
                event.internal = 1
                event.file = request.FILES['event_file']
                event.file_by = Student.objects.get(user=request.user.id)
                event.filename = request.FILES['event_file']
                event.save()


        elif 'external' in request.POST:
            student = Student.objects.get(user=request.user.id)
            if not 'event_id' in request.POST or request.POST['event_id'] == 'other':
                event = Events()
                event.e_name = request.POST['otherOption']
                event.start = datetime.strptime(
                    request.POST['otherOptionDate'], '%Y-%m-%dT%H:%M')
                event.year = request.POST['otherOptionDate'][0:4]
                if 'otherOptionSpeaker' in request.POST:
                    event.speaker = request.POST['otherOptionSpeaker']
                event.type = request.POST['otherOptionType']
                event.internal = 0
                event.save()

            else:
                event = Events.objects.get(id=request.POST['event_id'])

            if Event_Participants.objects.filter(student=student, event=event).exists():
                messages.error(
                request, "Commitment for this event is already uploaded. Please edit the previous submission.")
            else:         
                
                event_par = Event_Participants()
                event_par.event = event
                event_par.student = student
                event_par.position = request.POST['position']
                event_par.file = request.FILES['event_file']
                event_par.filename = request.FILES['event_file']
                event_par.save()

        elif 'internal_edit' in request.POST:
            print(request.POST)
            event = Events.objects.get(id=request.POST['internal_edit'])
            file_path = base_dir + event.file.url            
            event.file = request.FILES['event_file']
            event.filename = request.FILES['event_file']
            os.remove(file_path)
            event.save()

        elif 'external_edit' in request.POST:
            com = Event_Participants.objects.get(id=request.POST['external_edit'])
            com.position = request.POST['position']
            file_url = base_dir + com.file.url
            if 'file' in request.FILES:
                com.file = request.FILES['file']
                com.filename = request.FILES['file']
                os.remove(file_url)
            com.save()
        
        elif 'internal_delete' in request.POST:
            event = Events.objects.get(id=request.POST['internal_delete'])
            os.remove(base_dir + event.file.url)
            event.file = None
            event.filename = None
            event.file_by = None
            event.status = None
            event.save()
        
        elif 'external_delete' in request.POST:
            event_com = Event_Participants.objects.get(id=request.POST['external_delete'])
            os.remove(base_dir + event_com.file.url)
            event_com.file = None
            event_com.filename = None
            event_com.status = None
            event_com.position = None

            event_com.save()

        return redirect("upload-event")

    return render(request, "upload_event.html", context)


def submitOrgView(request):
    base_dir = str(settings.BASE_DIR).replace("\\", "/")
    student = Student.objects.get(user=request.user.id)
    orgs_in = Organisation.objects.filter(file_by=student).exclude(internal=0)
    orgs_ex = OrgComittee.objects.filter(student=student).exclude(org__internal=1)
    org_list_ex = Organisation.objects.filter(internal=0)
    context = {
        "page_name": "Upload Organisation Files",
        "orgs_ex": orgs_ex,
        "orgs_in": orgs_in,
        "org_list_ex":org_list_ex,
    }

    if request.POST:
        if 'internal' in request.POST:
            if not Organisation.objects.filter(name=request.POST['org_name'], year=request.POST['org_year']).exists():
                org = Organisation()
                org.name = request.POST['org_name']
                org.year = request.POST['org_year']            
                org.internal = 1 if 'internal' in request.POST else 0
                org.file = request.FILES['org_file']
                org.filename = request.FILES['org_file']
                org.file_by = student
                org.save()
            else:
                messages.error(
                    request, "Organisation comittee list was uploaded.")
        elif 'external' in request.POST:
            if 'org_id' in request.POST and not request.POST['org_id'] == 'other':
                org = Organisation.objects.get(id=request.POST['org_id'])
                if not OrgComittee.objects.filter(student=student, org=org).exists():
                    org_com = OrgComittee()
                    org_com.org = org
                    org_com.student = student
                    org_com.file = request.FILES['org_file']
                    org_com.filename = request.FILES['org_file']
                    org_com.position = request.POST['position']
                    org_com.save()
                else:
                    messages.error(
                    request, "Organisation commitment was uploaded.")

        
            else:
                org = Organisation()
                org.name = request.POST['org_name']
                org.year = request.POST['org_year']            
                org.internal = 0
                org.save()
                org_com = OrgComittee()                
                org_com.student = student
                org_com.org = org
                org_com.position = request.POST['position']
                org_com.file = request.FILES['org_file']
                org_com.filename = request.FILES['org_file']
                org_com.save()

        elif 'internal_edit' in request.POST:
            org = Organisation.objects.get(id=request.POST['internal_edit'])
            file_path = base_dir + org.file.url
            org.file = request.FILES['file']
            org.filename = request.FILES['file']
            os.remove(file_path)
            org.save()
        
        elif 'external_edit' in request.POST:
            org_com = OrgComittee.objects.get(id=request.POST['external_edit'])
            file_path = base_dir + org_com.file.url
            org_com.position = request.POST['position']
            if 'file' in request.FILES:
                org_com.file = request.FILES['file']
                org_com.filename = request.FILES['file']
                os.remove(file_path)
            org_com.save()

        elif 'internal_delete' in request.POST:
            org = Organisation.objects.get(id=request.POST['internal_delete'])
            file_path = base_dir + org.file.url
            os.remove(file_path)
            org.delete()
        
        elif 'external_delete' in request.POST:
            org_com = OrgComittee.objects.get(id=request.POST['external_delete'])
            file_path = base_dir + org_com.file.url
            os.remove(file_path)
            org_com.delete()

        return redirect("upload-org")
       

    return render(request, "upload_org.html", context)


def submitArticleView(request):
    student = Student.objects.get(user=request.user.id)
    arts = Article.objects.filter(student=student)
    base_dir = str(settings.BASE_DIR).replace("\\", "/")
    context = {
        "page_name": "Upload Articles",
        "arts": arts
    }
    if request.method == 'POST':
        print(request.POST)
        if 'art_submit' in request.POST or 'art_edit' in request.POST:
            student = Student.objects.get(user_id=request.user.id)
            print("In submit or edit")

            if 'art_submit' in request.POST:
                print("In submit")
                if Article.objects.filter(title=request.POST['art_title']).exists():
                    messages.error(request, "Article was uploaded.")
                    return redirect("upload-article")
                else:            
                    article = Article()
                    if request.POST['published'] == '0':
                        article.filename = request.FILES['proof']
                        article.file = request.FILES['proof']
                    else:
                        article.filename = request.FILES['art']
                        article.file = request.FILES['art']
            elif 'art_edit' in request.POST:
                print("In edit")
                article = Article.objects.get(id=request.POST['art_edit'])
                ori_file_url = base_dir + article.file.url
                if request.POST['published'] == '0' and 'proof_edit' in request.FILES:
                    os.remove(ori_file_url)
                    article.filename = request.FILES['proof_edit']
                    article.file = request.FILES['proof_edit']
                elif request.POST['published'] == '1' and 'article_edit' in request.FILES:
                    os.remove(ori_file_url)
                    article.filename = request.FILES['article_edit']
                    article.file = request.FILES['article_edit']

            article.title = request.POST['art_title']
            article.date = request.POST['art_year']
            article.type = request.POST['art_type']
            article.platform = request.POST['art_platform']
            article.comp = request.POST['art_comp']
            article.award = request.POST['art_awd']
            article.student = student
            article.published = request.POST['published']            
            article.save()              
            
            
        elif 'art_delete' in request.POST:
            print("In delete")
            art = Article.objects.get(id=request.POST['art_delete'])
            file_url = art.file.url
            print(file_url)
            file_path = base_dir + file_url
            print(file_path)
            os.remove(file_path)
            art.delete()
        return redirect ("upload-article")

    return render(request, "upload_article.html", context)

def submitOtherComp (request):
    base_dir = str(settings.BASE_DIR).replace("\\", "/")
    student = Student.objects.get(user_id=request.user.id)
    comps = OtherComp.objects.filter(student=student)
    context = {
        "comps": comps
    }
    if request.method == 'POST':
        if 'other_submit' in request.POST:
            comp = OtherComp()
            comp.name = request.POST['name']
            comp.year = request.POST['year']
            comp.award = request.POST['award']
            comp.file = request.FILES['file']
            comp.filename = request.FILES['file']
            comp.student = student
            comp.save()
        elif 'other_edit' in request.POST:
            comp = OtherComp.objects.get(id=request.POST['other_edit'])
            file_path = base_dir + comp.file.url
            comp.name = request.POST['name']
            comp.year = request.POST['year']
            comp.award = request.POST['award']
            if 'file' in request.FILES:
                comp.file = request.FILES['file']
                comp.filename = request.FILES['file']
                os.remove(file_path)
            comp.save()
        elif 'other_delete' in request.POST:
            comp = OtherComp.objects.get(id=request.POST['other_delete'])
            file_path = base_dir + comp.file.url
            os.remove(file_path)
            comp.delete()

        return redirect("upload-other")
    return render (request, "upload_other.html", context)

def download_excel(request, template_name):
    file_path = os.path.join(
        settings.BASE_DIR, 'media/template', template_name+'.xlsx')
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response


@login_required
@role_required(['SUPER ADMIN', 'ADMIN'])
def verEventView(request):
    base_dir =  str(settings.BASE_DIR).replace("\\", "/")
    pending_events = Events.objects.exclude(file__exact='').exclude(
        status__in=[0, 1]).exclude(file__exact=None).exclude(internal=0)
    approved_events = Events.objects.filter(status=1).exclude(internal=0)
    rejected_events = Events.objects.exclude(
        file__exact='').filter(status=0).exclude(file__exact=None).exclude(internal=0)

    pending_external = Event_Participants.objects.exclude(file__exact='').exclude(
        status__in=[0, 1]).exclude(file__exact=None).exclude(event__internal=1)
    approved_external = Event_Participants.objects.filter(status=1).exclude(event__internal=1)
    rejected_external = Event_Participants.objects.exclude(
        file__exact='').filter(status=0).exclude(file__exact=None).exclude(event__internal=1)

    pending_data = {
        'events': pending_events,  # Replace pending_orgs with your data
        'externals': pending_external,
        'pending': True,
    }
    approved_data = {
        'events': approved_events,  # Replace pending_orgs with your data
        'externals': approved_external,
        'pending': False,
    }
    rejected_data = {
        'events': rejected_events,  # Replace pending_orgs with your data
        'externals': rejected_external,
        'pending': False,
        "rejected": True,
    }

    context = {
        "page_name": "Verify Event Comittee",
        "pending_data": pending_data,
        "approved_data": approved_data,
        "rejected_data": rejected_data,
    }

    if request.POST:
        print(request.POST)
        if 'reject_in' in request.POST:
            event = Events.objects.get(id=request.POST['reject_in'])
            event.status = 0
            event.save()

        elif 'reject_ex' in request.POST:
            event_par = Event_Participants.objects.get(id=request.POST['reject_ex'])
            event_par.status = 0
            event_par.save()

        elif 'approve_in' in request.POST:
            print(request.POST)
          
            event = Events.objects.get(id=request.POST['approve_in'])
            event.status = 1
            
            file_url = event.file.url
            file_path = base_dir + file_url

            com_df = pd.read_excel(file_path,  names=["position", "matric"])
            
            for com in com_df.iterrows():
                print(com[1]['matric'].upper())
                if not Student.objects.filter(
                    matric_no=com[1]['matric'].upper()).exists():
                    messages.error(request, f"Matric number {com[1]['matric'].upper()} does not exist in the system. The committee list is not approved.")
                    return redirect("verify-event")
                else:
                    student = Student.objects.get(
                        matric_no=com[1]['matric'].upper())
                    if Event_Participants.objects.filter(event=event, student=student).exists():
                        event_par = Event_Participants.objects.get(
                            event=event, student=student)
                    else:
                        event_par = Event_Participants()
                        event_par.event = event
                        event_par.student = student
                    match_position = re.search(r'[A-Za-z\s]+', com[1]['position'])
                    event_par.position = match_position[0].strip()
                    event_par.status = 1
                    event_par.save()
            event.file = None
            event.filename= None
            os.remove(file_path)
            event.save()

        elif 'approve_ex' in request.POST:
            event_par = Event_Participants.objects.get(id=request.POST['approve_ex'])
            event_par.status = 1
            file_url = event_par.file.url
            file_path = base_dir + file_url  
            event_par.file = None  
            event_par.filename = None
            os.remove(file_path)
            event_par.save()
                       

           
        elif 'internal_delete' in request.POST:
            event = Events.objects.get(id=request.POST['internal_delete'])
            if Event_Participants.objects.filter(event=event).exists():
                event_com = Event_Participants.objects.filter(event=event)
                for com in event_com:
                    if com.registered == None and com.attendance == None:
                        com.delete()
                    else:
                        os.remove(base_dir + com.file.url) if com.file else None
                        com.file = None
                        com.filename = None
                        com.status = None            
                        com.save()
            os.remove(base_dir + event.file.url ) if event.file else None
            event.file = None
            event.filename = None
            event.file_by = None
            event.status = None            
            event.save()
            

        elif 'external_delete' in request.POST:
            com = Event_Participants.objects.get(id=request.POST['external_delete'])
            os.remove(base_dir + com.file.url) if com.file else None
            com.delete()
            
            

        return redirect("verify-event")

    return render(request, "verify_event.html", context)


@login_required
@role_required(['SUPER ADMIN', 'ADMIN'])
def verOrgView(request):
    base_dir = str(settings.BASE_DIR).replace("\\", "/")
    pending_orgs = Organisation.objects.exclude(file__exact='').exclude(
        status__in=[0, 1]).exclude(file__exact=None)
    approved_orgs = Organisation.objects.filter(status=1)
    rejected_orgs = Organisation.objects.exclude(
        file__exact='').filter(status=0).exclude(file__exact=None)
    
    pending_external = OrgComittee.objects.exclude(file__exact='').exclude(
        status__in=[0, 1]).exclude(file__exact=None).exclude(org__internal=1)
    approved_external = OrgComittee.objects.filter(status=1).exclude(org__internal=1)
    rejected_external = OrgComittee.objects.exclude(
        file__exact='').filter(status=0).exclude(file__exact=None).exclude(org__internal=1)

    
    pending_data = {
        'orgs': pending_orgs,  # Replace pending_orgs with your data
        'externals': pending_external,
        'pending': True,
    }
    approved_data = {
        'orgs': approved_orgs,  # Replace pending_orgs with your data
        'externals': approved_external,
        'pending': False,
    }
    rejected_data = {
        'orgs': rejected_orgs,  # Replace pending_orgs with your data
        'externals': rejected_external,
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
        if 'reject_in' in request.POST:
            org = Organisation.objects.get(id=request.POST['reject_in'])            
            org.status = 0
            org.save()
        elif'reject_ex' in request.POST:
            org_com = OrgComittee.objects.get(id=request.POST['reject_ex'])
            org_com.status = 0
            org_com.save()
        elif 'approve_in' in request.POST or 'approve_ex' in request.POST:
            base_dir = str(settings.BASE_DIR).replace("\\", "/")
            if 'approve_in' in request.POST:
                org = Organisation.objects.get(id=request.POST['approve_in'])
                org.status = 1

                file_url = org.file.url
                file_path = base_dir + file_url 
                com_df = pd.read_excel(
                    file_path,  names=["position", "matric"])
                
                for com in com_df.iterrows():
                    student = Student.objects.get(
                        matric_no=com[1]['matric'].upper())
                    if not Student.objects.filter(
                        matric_no=com[1]['matric'].upper()).exists():
                        messages.error(request, f"Matric number {com[1]['matric'].upper()} does not exist in the system. The committee list is not approved.")
                        return redirect("verify-org")
                    else:
                        student = Student.objects.get(
                            matric_no=com[1]['matric'].upper())
                        if OrgComittee.objects.filter(org=org, student=student).exists():
                            org_com = OrgComittee.objects.get(org=org, student=student)
                        else:
                            org_com = OrgComittee()
                            org_com.org = org
                            org_com.student = student
                        match_position = re.search(r'[A-Za-z\s]+', com[1]['position'])
                        org_com.position = match_position[0].strip()
                        org_com.status = 1
                        org_com.save()
                
                org.file = None
                org.save()
            else:
                org_com = OrgComittee.objects.get(id=request.POST['approve_ex'])
                org_com.status = 1
                file_url = org_com.file.url
                org_com.file = None 
                org_com.save()
                file_path = base_dir + file_url 
            os.remove(file_path) 

        elif 'delete_in' in request.POST:
            org = Organisation.objects.get(id=request.POST['delete_in'])
            if org.file:
                file_path = base_dir + org.file.url
                os.remove(file_path)
            org.delete()

        elif 'delete_ex' in request.POST:
            org_com = OrgComittee.objects.get(id=request.POST['delete_ex'])
            if org_com.file:
                file_path = base_dir + org_com.file.url
                os.remove(file_path)
            org_com.delete()

                 
        return redirect("verify-org")

    return render(request, "verify_org.html", context)


@login_required
@role_required(['SUPER ADMIN', 'ADMIN'])
def verArtView(request):
    base_dir = str(settings.BASE_DIR).replace("\\", "/")
    pending_arts = Article.objects.exclude(file__exact='').exclude(
        status__in=[0, 1]).exclude(file__exact=None)
    approved_arts = Article.objects.filter(status=1)
    rejected_arts = Article.objects.filter(status=0).exclude(file__exact='').exclude(file__exact=None)
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

    if request.method == 'POST':
        print(request.POST)
        if "art_reject" in request.POST:
            art = Article.objects.get(id=request.POST['art_reject'])
            art.status = 0
            art.save()
        elif "art_approve" in request.POST:
            art = Article.objects.get(id=request.POST['art_approve'])
            art.status = 1
            base_dir = str(settings.BASE_DIR).replace("\\", "/")
            file_url = art.file.url
            file_path = base_dir + file_url
            os.remove(file_path)
            art.file = None
            art.save()
        elif "art_delete" in request.POST:
            art = Article.objects.get(id=request.POST['art_delete'])
            art.delete()

        return redirect("verify-article")

    return render(request, "verify_art.html", context)

@login_required
@role_required(['SUPER ADMIN', 'ADMIN'])
def verOtherView (request):
    base_dir = str(settings.BASE_DIR).replace("\\", "/")
    pending_comps = OtherComp.objects.exclude(file__exact='').exclude(
        status__in=[0, 1]).exclude(file__exact=None)
    approved_comps = OtherComp.objects.filter(status=1)
    rejected_comps = OtherComp.objects.exclude(
        file__exact='').filter(status=0).exclude(file__exact=None)
    pending_data = {
        'comps': pending_comps,
        'pending': True,
    }
    approved_data = {
        'comps': approved_comps,
        'pending': False,
    }
    rejected_data = {
        'comps': rejected_comps,
        'pending': False,
        'rejected': True,
    }
    context = {
        "page_name": "Verify Co-curricular Awards",
        "pending_data": pending_data,
        "approved_data": approved_data,
        "rejected_data": rejected_data,

    }
    if request.method == 'POST':
        base_dir = str(settings.BASE_DIR).replace("\\", "/")
        if 'reject' in request.POST:
            comp = OtherComp.objects.get(id=request.POST['reject'])
            comp.status = 0
            comp.save()
        elif 'approve' in request.POST:
            comp = OtherComp.objects.get(id=request.POST['approve'])
            comp.status = 1
            file_url = comp.file.url
            file_path = base_dir + file_url
            comp.file = None
            comp.save()
            os.remove(file_path)

        elif 'other_delete' in request.POST:
            comp = OtherComp.objects.get(id=request.POST['other_delete'])
            if comp.file:
                file_path = base_dir + comp.file.url
                os.remove(file_path)
            comp.delete()
        
        return redirect ("verify-other")


    return render (request, "verify_other.html", context)

def statusView(request):
    student = Student.objects.get(user=request.user.id)
    events = Events.objects.filter(file_by=student).exclude(file__exact='')
    orgs = Organisation.objects.filter(file_by=student).exclude(file__exact='')
    arts = Article.objects.filter(student=student).exclude(file__exact='')
    context = {
        "page_name": "Upload Status",
        "events": events,
        "orgs": orgs,
        "arts": arts
    }
    return render(request, "status.html", context)

def get_art_details(request, art_id):
    print(art_id)
    try:
        art = Article.objects.get(id=art_id)
        print(art)
        # Retrieve the necessary event details

        response_data = {
            'id': art_id,
            'title': art.title,
            'date': art.date,
            'type': art.type,
            'platform': art.platform,
            'status': art.status,
            'comp': art.comp,
            'award': art.award,
            'file': art.file.url if art.file else None,
            'published': art.published,
            'filename': art.filename,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)
    
def get_internal_com_details(request, event_id):
    try:
        event = Events.objects.get(id=event_id)
        # Retrieve the necessary event details

        response_data = {
            'id': event_id,
            'e_name': event.e_name,
            'file': event.file.url,
            'filename': event.filename,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    
def get_external_com_details(request, com_id):
    try:
        com = Event_Participants.objects.get(id=com_id)
        # Retrieve the necessary event details

        response_data = {
            'id': com_id,
            'event_name': com.event.e_name,
            'position': com.position,
            'file': com.file.url,
            'status': com.status,
            'filename': com.filename,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Event Committeee not found'}, status=404)
    

def get_internal_org_details(request, org_id):
    try:
        org = Organisation.objects.get(id=org_id)
        # Retrieve the necessary event details

        response_data = {
            'id': org_id,
            'name': org.name,
            'year': org.year,
            'file': org.file.url,
            'filename': org.filename,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Organisation not found'}, status=404)
    
def get_external_org_details(request, org_com_id):
    try:
        com = OrgComittee.objects.get(id=org_com_id)
        # Retrieve the necessary event details

        response_data = {
            'id': org_com_id,
            'name': com.org.name,
            'year': com.org.year,
            'position': com.position,
            'file': com.file.url,
            'filename': com.filename,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Organisation Committeee not found'}, status=404)
    

def get_other_comp_details(request, comp_id):
    try:
        comp = OtherComp.objects.get(id=comp_id)
        # Retrieve the necessary event details

        response_data = {
            'id': comp_id,
            'name': comp.name,
            'year': comp.year,
            'award': comp.award,
            'file': comp.file.url,
            'filename': comp.filename,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Competition award not found'}, status=404)