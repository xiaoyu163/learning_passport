from django.shortcuts import render, redirect
from .models import Events, Event_Participants, Announcement
from django.conf import settings
from django.http import FileResponse
from users.models import User,Student
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os

# def examplePage(request):
#     return render (request, "try.html")

# Create your views here.
@login_required
def eventListView (request):
    # base_dir = settings.BASE_DIR
    # print("Base dir: ", base_dir)
    current_date = datetime.now()
    if request.user.role in 'STUDENT':
        events = Events.objects.filter(internal=1, start__gte=current_date).order_by("-start")
    else:
        events = Events.objects.filter(internal=1).order_by("-start")
    option_obj = Events.type.field.choices
    parts = list()
    if request.user.role in 'STUDENT':
        student = Student.objects.get(user_id=request.user.id)
        for event in events:
            part = Event_Participants.objects.filter(student=student, event=event).first()
            parts.append(part)
    else:
        parts = ''
    print(parts)
    event_parts = zip(events,parts)
  
    
    context = {
        "events": events,
        "event_parts": event_parts,
        "option_obj": option_obj,
    }
    if request.method == 'POST':
        if 'add_event' in request.POST or 'edit_event' in request.POST:
            if 'add_event' in request.POST:            
                event = Events()
            else:
                event = Events.objects.all().get(id=request.POST['event_id'])
            event.c_name = request.POST['event_name_c']
            event.e_name = request.POST['event_name_e']
            event.start = datetime.strptime(request.POST['event_start'], '%Y-%m-%dT%H:%M')
            event.end = datetime.strptime(request.POST['event_end'], '%Y-%m-%dT%H:%M')           
            event.year = request.POST['event_start'][0:4]
            event.venue = request.POST['event_venue']
            event.speaker = request.POST['event_speaker']
            event.type = request.POST['event_type']
            event.desc = request.POST['event_desc']
            event.internal = request.POST['internal']
            attendance = 1 if 'enable' in request.POST else 0
            print(request.FILES)
            if 'poster' in request.FILES:
                event.poster = request.FILES['poster']
            event.attendance = attendance
            event.save()

        elif 'register' in request.POST:
            print(request.POST)
            student = Student.objects.get(user_id=request.user.id)
            event = Events.objects.get(id=request.POST['event_id'])
            if not Event_Participants.objects.filter(student=student, event=event).exists():
                event_part = Event_Participants()
                event_part.event = event
                event_part.student = student
                event_part.registered = 1
            else:
                event_part = Event_Participants.objects.get(student=student, event=event)
                event_part.registered = 1
            
            event_part.save()
            print(event_part)
            return redirect("events")
        
        elif 'delete_event' in request.POST:            
            event_id = request.POST['event_id']
            event = Events.objects.get(id=event_id)
            parts = Event_Participants.objects.filter(event=event)
            if parts:
                parts.delete()
            
            event.delete()
            base_dir = str(settings.BASE_DIR).replace("\\","/")
            if event.file:
                file_url = event.file.url
                file_path = base_dir + file_url
                os.remove(file_path)
            if event.poster:
                poster_path = base_dir + event.poster.url
                os.remove(poster_path)

        return redirect ("events")
    return render (request, "event_list.html", context) 


def eventDetailView (request, id):
    event = Events.objects.get(id=id)
    if request.user.role in 'STUDENT':
        student = Student.objects.get(user_id=request.user.id)
        parts = Event_Participants.objects.get(student=student, event=event) if Event_Participants.objects.filter(student=student, event=event).exists() else None
        current_time = datetime.now()
        if event.enable_attendance == 1:
            curr_event = 1
        else:
            if event.start and event.end:
                if event.start.replace(tzinfo=None) <= current_time <= event.end.replace(tzinfo=None) and event.attendance==1:
                    curr_event = 1
                else:
                    curr_event = 0
            else:
                curr_event = 0
    else:
        parts = ''
        curr_event = 0
    context = {
        "event": event,
        "start_date": event.start.strftime("%d %b %Y") if event.start else None,
        "start_time": event.start.strftime("%I:%M %p") if event.start else None,
        "start_day": event.start.strftime("%A") if event.start else None,
        "end_date": event.end.strftime("%d %b %Y") if event.end else None,
        "end_time": event.end.strftime("%I:%M %p") if event.end else None,
        "end_day": event.end.strftime("%A") if event.end else None,
        "parts": parts,
        "curr_event" : curr_event,
        "page_name": "Event Detail"
    }
    if request.method == 'POST':
        print(request.POST)
        if "register" in request.POST:
            student = Student.objects.get(user=request.user.id)
            event_part = Event_Participants()
            event_part.event = event
            event_part.student = student
            event_part.registered = 1
            event_part.save()
            return redirect("events")
        
        elif "poster" in request.POST:
            event.poster = request.FILES['poster']
            event.save()
            return redirect (request.get_full_path())

        elif 'attendance' in request.POST:      
            attendance = Event_Participants.objects.get(student=student, event=event)
            attendance.event = event            
            attendance.attendance = 1
            attendance.save()
            return redirect (request.get_full_path())
       
    return render (request, "event_detail.html", context)

@login_required
def takeAttendanceView (request):
    if request.user.role in 'STUDENT':
        # To store event that attendance are currently available
        events = list()
        student = Student.objects.get(user=request.user.id)
        parts = Event_Participants.objects.filter(student=student, registered=1)
        # To store registered event that are currently not available for attendance
        reg_events = list()
        current_time = datetime.now()
        for part in parts:
            print(part)
            start_time = part.event.start.replace(tzinfo=None) if part.event.start else None
            end_time = part.event.end.replace(tzinfo=None) if part.event.end else None
            if part.event.enable_attendance==1:
                events.append(part)
            elif start_time and end_time :
                if start_time <= current_time <= end_time and part.event.attendance==1:
                    events.append(part)
                else:
                    reg_events.append(part)
            else:
                    reg_events.append(part)
            
        # parts = parts.filter(event__in=events)
        print("Participation")
        print(parts)
        print("Event")
        print(events)
        # par_events = zip(parts, events)
        context = {
           
            "events": events,
            "reg_events": reg_events,
            "page_name": "Registered Event"
        }
    elif request.user.role in 'SUPER ADMIN':
        all_event = Events.objects.order_by("-start")
        att_event = list()
        for event in all_event:
            current_time = datetime.now()
            start = event.start.replace(tzinfo=None) if event.start else None
            end = event.end.replace(tzinfo=None) if event.end else None
            if event.enable_attendance == 1:
                att_event.append(event)
            elif start and end:
                if start <= current_time <= end:
                    att_event.append(event)
                
                
        
        context = {
            "all_event": all_event,
            "att_event": att_event,
        }
    if request.method == 'POST':
        
        if 'attendance' in request.POST:
            print(request.POST)
            event = Events.objects.get(id=request.POST['event_id'])         
            attendance = Event_Participants.objects.get(student=student, event=event)
            attendance.event = event            
            attendance.attendance = 1
            attendance.save()
            return redirect("attendance")
    return render (request, "attendance.html", context)

def adminAttendaceView (request, event_id):
    event = Events.objects.get(id=event_id)
    par_id = list()
    participants = Event_Participants.objects.filter(event_id=event_id, attendance=1)
    for par in participants:
        par_id.append(par.student_id)
    students = Student.objects.filter(user__is_active=True).exclude(id__in=par_id)
   
    context = {
        "event": event,
        "participants": participants,
        "students": students
    }
    if request.method == 'POST':
        if 'enable' in request.POST:
            event = Events.objects.get(id=request.POST['enable'])
            event.enable_attendance = 1
            event.save()
        elif 'disable' in request.POST:
            event = Events.objects.get(id=request.POST['disable'])
            event.enable_attendance = 0
            event.save()
        else:
            for elem in request.POST:
                if elem.isnumeric():
                    elem = int(elem)
        
                    if Event_Participants.objects.filter(student_id=elem, event_id=event_id).exists():
                        par = Event_Participants.objects.get(student_id=elem, event_id=event_id)
                    else:
                        par = Event_Participants()
                        par.student_id = elem
                        par.event_id = event_id
                    par.attendance = 1
                    par.save()
            for par in participants:
                if str(par.student_id) not in request.POST:
                    par.attendance = 0
                    par.save()
        return redirect ("admin-attendance", event_id=event_id)
    return render (request, "admin_attendance.html", context)

def get_event_details(request, event_id):
    try:
        event = Events.objects.get(id=event_id)
        # Retrieve the necessary event details

        response_data = {
            'id': event_id,
            'e_name': event.e_name,
            'c_name': event.c_name,
            'type': event.type,
            'start': event.start,
            'end': event.end,
            'venue': event.venue,
            'desc': event.desc,
            'internal': event.internal,
            'speaker': event.speaker,
            'attendance': event.attendance,
            'on_time': event.enable_attendance,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@login_required
def announcementListView(request):
    if request.user.role in 'SUPER ADMIN':
        anns = Announcement.objects.all().order_by("-created_time")
        general_anns = Announcement.objects.filter(category=1).order_by("-created_time")
        event_anns = Announcement.objects.filter(category=2).order_by("-created_time")
        others_anns = Announcement.objects.filter(category=3).order_by("-created_time")
    else:
        program = Student.objects.get(user=request.user.id).program
        if program == 1:
            anns = Announcement.objects.all().filter(display_to__in=[1,2]).order_by("-created_time")
            general_anns = Announcement.objects.filter(category=1, display_to__in=[1,2]).order_by("-created_time")
            event_anns = Announcement.objects.filter(category=2, display_to__in=[1,2]).order_by("-created_time")
            others_anns = Announcement.objects.filter(category=3, display_to__in=[1,2]).order_by("-created_time")
        else:
            anns = Announcement.objects.all().filter(display_to__in=[1,3]).order_by("-created_time")
            general_anns = Announcement.objects.filter(category=1, display_to__in=[1,3]).order_by("-created_time")
            event_anns = Announcement.objects.filter(category=2, display_to__in=[1,3]).order_by("-created_time")
            others_anns = Announcement.objects.filter(category=3, display_to__in=[1,3]).order_by("-created_time")
    cat_obj = Announcement.category.field.choices
    for_obj = Announcement.display_to.field.choices
    if request.method == "POST":
        if 'add_ann' in request.POST:
            ann = Announcement()
            ann.title = request.POST['title']
            ann.content = request.POST['content']
            ann.category = request.POST['type']
            ann.display_to = request.POST['for']
            ann.user = request.user
            ann.save()

        elif 'edit_ann' in request.POST:
            print(request.POST)
            ann = Announcement.objects.get(id=request.POST['ann_id'])
            ann.title = request.POST['ann_title']
            ann.content = request.POST['ann_content']
            ann.category = request.POST['ann_type']
            ann.display_to = request.POST['ann_for']
            ann.user = request.user
            ann.save()

        elif 'delete_ann' in request.POST:
            ann = Announcement.objects.get(id=request.POST['ann_id'])          
            ann.delete()
 

        return redirect ("announcements")


    context = {
        "anns": anns,
        "general_anns": general_anns,
        "event_anns": event_anns,
        "others_anns": others_anns,
        "cat_obj": cat_obj,
        "for_obj": for_obj,
    }
    return render (request, "announcement.html", context)

def get_ann_details(request, ann_id):
    try:
        ann = Announcement.objects.get(id=ann_id)
        # Retrieve the necessary event details

        response_data = {
            'id': ann_id,
            'title': ann.title,
            'content': ann.content,
            'category': ann.category,
            'display_to': ann.display_to,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Announcement not found'}, status=404)