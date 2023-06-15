from django.shortcuts import render, redirect
from .models import Events, Event_Participants
from users.models import User,Student
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

def eventListView (request):
    events = Events.objects.all().order_by("-id")
    option_obj = Events.type.field.choices
    parts = list()
    if request.user.role in 'STUDENT':
        student = Student.objects.get(user=request.user.id)
        for event in events:
            part = Event_Participants.objects.filter(student=student, event=event).first()
            parts.append(part)
    else:
        parts = ''

    event_parts = zip(events,parts)
  
    
    context = {
        "events": events,
        "event_parts": event_parts,
        "option_obj": option_obj,
        "page_name": "Events",
    }
    if request.method == 'POST':
        print(request.POST)
        if 'add_event' in request.POST or 'edit_event' in request.POST:
            if 'add_event' in request.POST:            
                event = Events()
            else:
                event = Events.objects.all().get(id=request.POST['event_id'])
                event = Events()
            event.c_name = request.POST['event_name_c']
            event.e_name = request.POST['event_name_e']
            event.start = datetime.strptime(request.POST['event_start'], '%Y-%m-%dT%H:%M')
            event.end = datetime.strptime(request.POST['event_end'], '%Y-%m-%dT%H:%M')
            event.venue = request.POST['event_venue']
            event.speaker = request.POST['event_speaker']
            event.type = request.POST['event_type']
            event.desc = request.POST['event_desc']
            event.internal = request.POST['internal']
            attendance = 1 if 'enable' in request.POST else 0
            event.attendance = attendance
            event.save()

        elif 'register' in request.POST:
            print(request.POST)
            student = Student.objects.get(user=request.user.id)
            event = Events.objects.get(id=request.POST['event_id'])
            event_part = Event_Participants()
            event_part.event = event
            event_part.student = student
            event_part.registered = 1
            print(event_part)
            event_part.save()
            return redirect("registered")

        return redirect ("events")
    return render (request, "event_list.html", context) 

def eventDetailView (request, id):
    event = Events.objects.get(id=id)
    if request.user.role in 'STUDENT':
        student = Student.objects.get(user=request.user.id)
        print(student)
        parts = Event_Participants.objects.filter(student=student, event=event)
        print(parts)
    else:
        parts = ''
    context = {
        "event": event,
        "start_date": event.start.strftime("%d %b %Y"),
        "start_time": event.start.strftime("%I:%M %p"),
        "start_day": event.start.strftime("%A"),
        "end_date": event.end.strftime("%d %b %Y"),
        "end_time": event.end.strftime("%I:%M %p"),
        "end_day": event.end.strftime("%A"),
        "parts": parts
    }
    if request.method == 'POST':
        student = Student.objects.get(user=request.user.id)
        event_part = Event_Participants()
        event_part.event = event
        event_part.student = student
        event_part.registered = 1
        event_part.save()
        return redirect("registered")
       
    return render (request, "event_detail.html", context)

@login_required
def eventRegisteredView (request):
    if request.user.role in 'STUDENT':
        student = Student.objects.get(user=request.user.id)
        parts = Event_Participants.objects.filter(student=student)
        events = list()
        for i in parts:
            events.append(Events.objects.get(id=i.event_id))
    
        par_events = zip(parts, events)
        context = {
            "par_events": par_events,
            "events": events,
            "page_name": "Registered Event"
        }

    if request.method == 'POST':
        
        if 'attendance' in request.POST:
            print(request.POST)
            event = Events.objects.get(id=request.POST['event_id'])         
            attendance = Event_Participants.objects.get(student=student, event=event)
            attendance.event = event            
            attendance.attendance = 1
            attendance.save()
            return redirect("registered")
    return render (request, "event_list.html", context)

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
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)