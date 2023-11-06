from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from learning_passport import settings
from .models import User, Student, Lecturer, OrgComittee, Semester, Organisation
from events.models import Event_Participants,OtherComp, Events, Announcement
from articles.models import Article
from django.contrib.auth.hashers import make_password
from datetime import datetime

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponse
import pdfkit
from django.template.loader import get_template
from django.urls import reverse
import os
# from weasyprint import HTML
from django.http import HttpResponse
from django.http import JsonResponse

import pandas as pd

import re
from datetime import date

import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')

# Create your views here.

def addStudentsView (request):
    if request.POST:
        student_list = request.FILES['student']
        df = pd.read_excel(student_list, names=["matric","282","283","33","284","285","286","287","288","289"])
        attend = list()
      
        for event in df.iterrows():
            matric = str(event[1]['matric']).upper()
            student = Student.objects.get(matric_no=matric)
            attend.append(282) if event[1]['282'] == 1 else None
            attend.append(283) if event[1]['283'] == 1 else None
            attend.append(284) if event[1]['284'] == 1 else None
            attend.append(285) if event[1]['285'] == 1 else None
            attend.append(286) if event[1]['286'] == 1 else None
            attend.append(287) if event[1]['287'] == 1 else None
            attend.append(288) if event[1]['288'] == 1 else None
            attend.append(289) if event[1]['289'] == 1 else None
            attend.append(33) if event[1]['33'] == 1 else None
            print(attend)
            for id in attend:
                if Event_Participants.objects.filter(student=student, event_id=id).exists():
                    par = Event_Participants.objects.get(student=student, event_id=id)
                else:
                    par = Event_Participants()
                    par.student = student
                    par.event_id = id
                par.attendance = 1
                par.save()
            attend = list()
            
    return render (request, "add_student.html")
def loginView(request):

    login_page = 'login.html'

    redirected_login_failed_link = 'login'

    redirected_success_link_dict = {
        'SUPER ADMIN' : 'dashboard',
        'ADMIN' : 'dashboard',
        'HEAD OF DEPARTMENT' : 'dashboard',
        'LECTURER' : 'dashboard',
        'STUDENT' : 'dashboard',
    }

    if request.method == 'POST':

        email = request.POST['email'].strip()
        password = request.POST['password'].strip()

        try:  
            user = User.objects.get(email=email)

        except ObjectDoesNotExist:
            messages.error(request, 'Account does not exist.')
            return redirect(redirected_login_failed_link)

        if not user.check_password(password):
            messages.error(request, "Incorrect username or password.")
            return redirect(redirected_login_failed_link)
        else:  # if password correct
            login(request, user)
            messages.success(request, f"Welcome {user.full_name}.")
        
            if 'next' in request.GET:
                if request.GET['next'] != '/':
                    return redirect(request.GET['next'])

            return redirect(redirected_success_link_dict[user.role])
  
 # redirect if logged in 
    if request.user.is_authenticated:
        redirected_link = redirected_success_link_dict[request.user.role]
        return redirect(redirected_link)
 
    return render(request, login_page)



@login_required
def logoutView(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect('login')

def registerView(request):
    option_position = Lecturer.position.field.choices
    context = {
        "option_position": option_position,
    }
    if request.method == 'POST':
        print(request.POST)
        email = request.POST['email']


        if User.objects.filter(email=email):
            messages.info(request, "Account already exist. Please proceed to login.")
            return redirect('login')
        
        else:
            role = request.POST['role']
            new_user = User()
            new_user.email = email
            new_user.password = make_password(request.POST['password'])
            new_user.role = role
            new_user.full_name = request.POST['name'].upper()
                  
        
            if new_user.role not in 'STUDENT':
                lecturer = Lecturer()
                lecturer.user = new_user
                lecturer.position = request.POST['lecturer_position']
                new_user.save()
                lecturer.save()
                messages.success(request,"Your account is registered successfully. Please proceed to login.")
                return redirect('login')
            
            else:
                new_user.save()
                id = new_user.id 
                return redirect('edit-profile', id=id)
    
    return render(request, "register.html", context)

def editProfile(request, id):
    student = Student.objects.get(user_id=id) if Student.objects.filter(user_id=id).exists() else None
    enrol_year = str(student.enrol_year)[0:7] if student else None
    grad_year = str(student.grad_year)[0:7] if student else None
    user = User.objects.get(id=id)
    lecturers = Lecturer.objects.filter(user__is_active=1)
    context = {
        "matric": user.email.split('@')[0].upper(),
        "name": user.full_name,
        "lecturers": lecturers,
        "student": student,
        "enrol_year": enrol_year,
        "grad_year": grad_year,
    }
    

    if request.method == 'POST':
        student = Student()
        student.user = user
        student.matric_no = request.POST['matric'].upper()
        student.program = request.POST['program']
        student.enrol_year = datetime.strptime(request.POST['enrol'], '%Y-%m').date()
        student.grad_year = datetime.strptime(request.POST['grad'], '%Y-%m').date()
        student.lecturer_id = request.POST['lecturer']
        student.save()
        user = User.objects.get(id=id)
        user.full_name = request.POST['name'].upper()
        user.contact = request.POST['contact']
        user.address = request.POST['address']
        user.save()

        messages.success(request,"Your account is registered successfully. Please proceed to login.")
        return redirect('login')
        
    return render(request, "edit_profile.html", context)

def manageStudent (request):
    lecturers = Lecturer.objects.all()
    students = Student.objects.all()
    context = {
        "students": students,
        "lecturers": lecturers,
    }

    if request.method == "POST":
        current_date = datetime.now().date()
        if 'manage-student' in request.POST:
            student = Student.objects.get(id=request.POST['manage-student'])
            student.user.full_name = request.POST['student_name'].upper()
            student.matric_no = request.POST['student_matric'].upper()
            student.enrol_year = datetime.strptime(request.POST['student_enrol'], '%Y-%m').date()
            student.grad_year = datetime.strptime(request.POST['student_grad'], '%Y-%m').date()
            student.user.is_active = 1 if 'student_active' in request.POST else 0
            student.lecturer_id = request.POST['student_lect']
            student.save()
            student.user.save()

        if 'delete-student' in request.POST:
            student = Student.objects.get(id=request.POST['delete-student'])
            student.delete()
            student.user.delete()

        if 'update-status' in request.POST:            
            users = User.objects.filter(role="STUDENT", is_active=1)
            current_year = Semester.objects.filter(end__gte=current_date, start__lte=current_date).first()
            print(users.count())
            print(current_year.academic_year)
            for user in users:
                student = Student.objects.get(user=user)
                if student.grad_year <= current_year.start:
                    user.is_active = 0
                    user.save()
            messages.success (request, f"Student status updated succesfully for Semester {current_year.semester} {current_year.academic_year}")
        
        return redirect ("manage-student")
    return render (request, "manage_student.html", context)

def manageLecturer (request):
    lecturers = Lecturer.objects.all()
    student_counts = list()
    for lecturer in lecturers:
        student_counts.append(Student.objects.filter(lecturer=lecturer).count())
    option_position = Lecturer.position.field.choices
    lecturers_students = zip(lecturers,student_counts)
    context = {
        "lecturers_students": lecturers_students,
        "option_position": option_position,

    }

    if request.POST:
        if 'manage-lecturer' in request.POST:
            lecturer = Lecturer.objects.get(id=request.POST['manage-lecturer'])
            lecturer.position = request.POST['lecturer_position']
            lecturer.user.full_name = request.POST['lecturer_name'].upper()
            lecturer.user.is_active = 1 if 'lecturer_active' in request.POST else 0
            lecturer.save()
            lecturer.user.save()
        elif 'delete-lecturer' in request.POST:
            lecturer = Lecturer.objects.get(id=request.POST['delete-lecturer'])
            lecturer.delete()
        return redirect ("manage-lecturer")
    return render (request,"manage_lecturer.html", context)

def resetPasswordView(request):

    context = {
        "page_name": "Change Password",
    }

    if request.method == 'POST':
        old_pw = request.POST['old_pw']        
        new_pw = request.POST['new_pw']
        if not request.user.check_password(old_pw):
            print("incorrect")
            messages.error(request, "Incorrect existing password!")
            return redirect("change-password")
        else:
            user = User.objects.get(id=request.user.id)
            user.password = make_password(new_pw)
            user.save()
            logout(request)
            messages.success(request, "Password changed successfully. Please login again.")
            return redirect ("login")
    return render (request, "change_password.html",context)

@login_required
def generateTranscriptView(request, user_id):
    if Student.objects.filter(user_id=user_id).exists():
        student = Student.objects.get(user_id=user_id) 

        # Event Participation
        event_pars_in = Event_Participants.objects.filter(student=student, attendance=1, event__internal=1).order_by('event__type')
        event_pars_ex = Event_Participants.objects.filter(student=student, attendance=1, event__internal=0).order_by('event__type')
        arts = Article.objects.filter(student=student, status=1)
        awarded_arts = arts.filter(award__isnull=False).exclude(award__exact="").exclude(award__exact=None)
        
        # Event/Org Committee
        event_coms_in = Event_Participants.objects.filter(student=student, status=1, position__isnull=False, event__internal=1).order_by('event__start')
        event_coms_ex = Event_Participants.objects.filter(student=student, status=1, position__isnull=False, event__internal=0).order_by('event__start')
        org_coms_in = OrgComittee.objects.filter(student=student, org__internal=1, status=1).order_by('org__year')
        org_coms_ex = OrgComittee.objects.filter(student=student, org__internal=0, status=1).order_by('org__year')
        total_in_length = len(event_coms_in) + len(org_coms_in)
        total_ex_length = len(event_coms_ex) + len(org_coms_ex)

        hod_name = User.objects.get(role="HEAD OF DEPARTMENT").full_name

        # Other Competition
        other = OtherComp.objects.filter(student=student, status=1)
        context = {
            "student": student,
            "event_pars_in": event_pars_in,
            "event_pars_ex": event_pars_ex,
            "event_coms_in": event_coms_in,
            "event_coms_ex": event_coms_ex,
            "org_coms_in": org_coms_in,
            "org_coms_ex": org_coms_ex,
            "total_in_length": total_in_length,
            "total_ex_length": total_ex_length,
            "arts": arts,
            "awarded_arts": awarded_arts,
            "other": other,
            "transcript": True,
            "hod_name": hod_name,
        }

    else:
        context = {
            "transcript": False,
        }
    if request.method == 'POST':
        if Student.objects.filter(matric_no=request.POST['matric']).exists():

            student = Student.objects.get(matric_no=request.POST['matric'])
            user_id = student.user_id
        
        else:
            messages.error(request, "Student does not exists. Please enter a valid matric number.")
            return redirect ("generate-transcript", user_id=request.user.id)

        return redirect ("generate-transcript", user_id=user_id)

    return render (request,"generate_transcript.html", context)

@login_required
def dashboardView(request):
    current_date = datetime.now().date()
    if request.user.role in 'SUPER ADMIN':
    
        year_list = list()
        par_list = list()

        years = Semester.objects.values('academic_year').distinct()

        
        current_year = Semester.objects.filter(end__gte=current_date, start__lte=current_date).first()
        selected_year = current_year
        event_selection = Events.objects.values('e_name').distinct()
        event_name = Events.objects.all().first().e_name
        upcoming_events = Events.objects.filter(start__gte=current_year.start)
        selected = event_name
        events = Events.objects.filter(e_name=event_name)
        upcoming_events = Events.objects.filter(start__gte=current_date).order_by("start")[:2]
        announcements = Announcement.objects.order_by("-created_time")[:2]
        num_active = User.objects.filter(role='STUDENT', is_active=1).count()
        num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
        num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end).count()
        print(Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end))
        study_level = 1
        
        if request.method == 'POST':
            print(request.POST)
            if 'event_name' in request.POST:
                events = Events.objects.filter(e_name=request.POST['event_name']).order_by("year")
                print("events: ", events)
                event_name = request.POST['event_name']
                selected = event_name

            if 'academic_year' in request.POST or 'semester' in request.POST or 'study_level' in request.POST:
                count_active = 0
                study_level = request.POST['study_level']
                if Semester.objects.filter(academic_year=request.POST['academic_year'], semester=request.POST['semester']).exists():
                    selected_year = Semester.objects.get(academic_year=request.POST['academic_year'], semester=request.POST['semester'])
                    
                else:
                    selected_year = Semester.objects.get(academic_year=request.POST['academic_year'])

                if study_level == '1':
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end).count()
                elif study_level == '2':
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end,student__program=1).count()
                else:
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end).exclude(student__program=1).count()

                if selected_year == current_year:
                    active = User.objects.filter(role='STUDENT', is_active=1)
                    
                    if request.POST['study_level'] == '1':
                        num_active = active.count()
                    elif request.POST['study_level'] == '2':
                        student = Student.objects.filter(user__in=active)
                        num_active = student.filter(program=1).count()
                    else:
                        student = Student.objects.filter(user__in=active)
                        num_active = student.exclude(program=1).count()
                else:
                    users = User.objects.filter(role="STUDENT")
                    
                    for user in users:
                        student = Student.objects.get(user=user)
                        if student.grad_year > selected_year.start and student.enrol_year < selected_year.end:
                            if study_level == '1':
                                count_active += 1
                            elif study_level == '2':
                                count_active += 1 if student.program == 1 else 0
                            else:
                                count_active += 1 if not student.program == 1 else 0                    
                    
                    num_active = count_active
            
                return redirect ("dashboard")
            
        for event in events:
            year_list.append(event.year)
            number = Event_Participants.objects.filter(event=event, attendance=1).count()
            par_list.append(number) 
    
        print(par_list)
        par_df = pd.DataFrame({'Year':year_list, 'Participants': par_list})
        fig = px.line(par_df, x="Year", y="Participants", title=f'Number of Participants for {event_name}')
        fig.update_traces(mode="lines+markers")
        fig.update_xaxes(tickvals=year_list)
        fig.update_yaxes(dtick=1)
        graph_json = fig.to_json()


        context = {
            "graph_json": graph_json,
            "event_selection": event_selection,
            "selected": selected,
            "selected_year": selected_year,
            "years": years,
            "num_active": num_active,
            "study_level": study_level,
            "num_event": num_event,
            "num_article": num_article,
            "upcoming_events": upcoming_events,
            "announcements": announcements,
        }

    
        return render(request, "dashboard_admin.html", context)
    
    elif request.user.role in 'STUDENT':
        student = Student.objects.get(user_id=request.user.id)
        registered = Event_Participants.objects.filter(registered=1, student=student, event__start__gte=current_date).order_by("event__start")[:2]
        registered_events = list()
        for par in registered:
                registered_events.append(par.event)
        if student.program == 1:
            announcements = Announcement.objects.exclude(display_to=3).order_by("-created_time")[:2]
        else:
            announcements = Announcement.objects.exclude(display_to=2).order_by("-created_time")[:2]
        par_count = Event_Participants.objects.filter(student=student, attendance=1).count()
        com_count = Event_Participants.objects.filter(student=student, position__isnull=False, status=1).count()
        org_count = OrgComittee.objects.filter(student=student, status=1).count()
        art_count = Article.objects.filter(student=student, status=1).count()
        context = { 
            "student": student,
            "announcements": announcements,
            "registered_events": registered_events,
            "par_count": par_count,
            "com_count": com_count,
            "org_count": org_count,
            "art_count": art_count,
        }
        return render(request, "dashboard_student.html", context)
    
    else:
        context = {

        }
        return render (request, "dashboard_lecturer.html", context)

def semesterDatesView (request):
    current_date = datetime.now().date()
    current_sem = Semester.objects.filter(end__gte=current_date, start__lte=current_date).first()
    semesters = Semester.objects.all()
    context = {
        "curr_sem": current_sem,
        "semesters": semesters,
    }
    if request.method == 'POST':
        if 'add-semester' in request.POST:
            academic_year = request.POST['academic_year']
            semester = request.POST['semester']
            if not Semester.objects.filter(academic_year=academic_year, semester=semester).exists():
                sem = Semester()
                sem.academic_year = academic_year
                sem.semester = semester
                sem.start = request.POST['start']
                sem.end = request.POST['end']
                sem.save()
            else:
                messages.error(request, f'Semester {semester} Year {academic_year} already exists.')
        
        if 'delete' in request.POST:
            sem = Semester.objects.get(id=request.POST['delete'])
            sem.delete()
        return redirect ("semesters")
    return render (request, "semester.html", context)
def get_student_details(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        # Retrieve the necessary event details

        response_data = {
            'id': student_id,
            'matric': student.matric_no,
            'name': student.user.full_name,
            'enrol': student.enrol_year,
            'grad': student.grad_year,
            'active': student.user.is_active,
            'student_lect': student.lecturer_id
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    

def get_lecturer_details(request, lecturer_id):
    try:
        lecturer = Lecturer.objects.get(id=lecturer_id)
        # Retrieve the necessary event details

        response_data = {
            'id': lecturer_id,
            'name': lecturer.user.full_name,
            'position': lecturer.position,
            'active': lecturer.user.is_active,
            # Include other event details in the response as needed
        }
        return JsonResponse(response_data)
    except Events.DoesNotExist:
        return JsonResponse({'error': 'Lecturer not found'}, status=404)