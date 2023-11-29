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
from datetime import datetime
from django.http import FileResponse

import openpyxl
from openpyxl.styles import Alignment

import pandas as pd
import zipfile
import re
from datetime import date
from io import BytesIO
from xhtml2pdf import pisa
import matplotlib.pyplot as plt
import plotly.express as px
import base64
from docxtpl import DocxTemplate
from docx import Document
from htmldocx import HtmlToDocx
from bs4 import BeautifulSoup
import pdfkit

import asyncio
# from pyppeteer import launch
from weasyprint import HTML
from flask import Flask, send_file
import os
import subprocess
from subprocess import run
import pypandoc
import tempfile
from tempfile import NamedTemporaryFile
from django.template.loader import render_to_string

base_dir = str(settings.BASE_DIR).replace("\\", "/")

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
def contentPDF(request, student_id):
    student = Student.objects.get(id=student_id) 
    current_date = datetime.now().date()
    current_year = Semester.objects.filter(end__gte=current_date, start__lte=current_date).first()
    # Event Participation
    event_pars_in = Event_Participants.objects.filter(student=student, attendance=1, event__internal=1).order_by('event__type')
    event_pars_ex = Event_Participants.objects.filter(student=student, attendance=1, event__internal=0).order_by('event__type')
    arts = Article.objects.filter(student=student, status=1, published__isnull=False)
    awarded_arts = Article.objects.filter(published__isnull=True)
    
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
        "event_in_post": event_pars_in.filter(event__type__in=[1,2,3,4]),
        "event_ex_post": event_pars_ex.filter(event__type__in=[1,2]),
        "event_in_others": event_pars_in.exclude(event__type__in=[1,2,3,4]),
        "event_ex_others": event_pars_ex.exclude(event__type__in=[1,2]),
        "org_coms_in": org_coms_in,
        "org_coms_ex": org_coms_ex,
        "total_in_length": total_in_length,
        "total_ex_length": total_ex_length,
        "arts": arts,
        "awarded_arts": awarded_arts,
        "other": other,
        "transcript": True,
        "hod_name": hod_name,
        "current": current_year
    }
    if student.program == 1:
        dynamic_html_content = render_to_string('pdf_undergrad.html', context)  
    else:
        dynamic_html_content = render_to_string('pdf_postgrad.html', context)
    htmldoc = HTML(string=dynamic_html_content, base_url=request.build_absolute_uri())
    # pdf_path = f'{student.matric_no}_transcript.pdf'
    pdf_bytes = htmldoc.write_pdf()

    # Specify the filename for the downloadable file
    pdf_filename = f'{student.matric_no}_transcript.pdf'

    


    return pdf_bytes, pdf_filename
    # return redirect ("generate-transcript", student.user.id)

def generatePDF (request, student_id):
    pdf_bytes, pdf_filename = contentPDF(request, student_id)
    # Send the PDF as a downloadable file
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'

    return response

def download_all_transcripts(request, semester_id):
    print('Download all')
    # Assuming you have a list of student IDs
    semester = Semester.objects.get(id=semester_id)
    students = Student.objects.filter(grad_sem=semester)

    # Create a BytesIO object to store the zipped content
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'a') as zip_file:
        for student in students:
            # Generate a single student transcript PDF
            pdf_bytes, pdf_filename = contentPDF(request,student.id)

            # Add the PDF content to the zip file
            zip_file.writestr(pdf_filename, pdf_bytes)

    # Close the zip file
    zip_buffer.seek(0)

    # Create a Django HttpResponse with the zip file content
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=all_transcripts.zip'
    return response

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
    current_date = datetime.now().date()
    current_sem = Semester.objects.filter(end__gte=current_date, start__lte=current_date).first()
    option_position = Lecturer.position.field.choices
    option_program = Student.program.field.choices
    lecturers = Lecturer.objects.filter(user__is_active=1)

    context = {
        "option_position": option_position,
        "option_program": option_program,
        "lecturers": lecturers,
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
                new_user.contact = request.POST['contact']
                new_user.address = request.POST['address']
                new_user.save()
                id = new_user.id
                student = Student()
                student.user_id = id
                student.matric_no = new_user.email.split('@')[0].upper()
                print(request.POST['program'])
                student.program = request.POST['program']
                student.enrol_sem = current_sem
                if student.program == '1':
                    grad_year = int(current_sem.academic_year.split('/')[0]) + 3
                    grad_year = str(grad_year) + '/' + f'{grad_year+1}'[2:]
                    grad_sem = current_sem.semester
                    
                elif student.program == '2' or student.program == '3':
                    grad_year = int(current_sem.academic_year.split('/')[0]) + 1
                    grad_year = str(grad_year) + '/' + f'{grad_year+1}'[2:]
                    grad_sem = 2 if current_sem.semester == 1 else 1
                else:
                    grad_year = int(current_sem.academic_year.split('/')[0]) + 2
                    grad_year = str(grad_year) + '/' + f'{grad_year+1}'[2:]
                    grad_sem = 2 if current_sem.semester == 1 else 1
                if Semester.objects.filter(academic_year=grad_year, semester=grad_sem).exists():
                    grad_semester = Semester.objects.get(academic_year=grad_year, semester=grad_sem)
                else:
                    grad_semester = Semester()
                    grad_semester.academic_year = grad_year
                    grad_semester.semester = grad_sem
                    grad_semester.save()
                student.lecturer = Lecturer.objects.get(user__role='HEAD OF DEPARTMENT')
                student.grad_sem = grad_semester
                student.save()

                messages.success(request,"Your account is registered successfully. Please proceed to login.")
                return redirect('login')
    
    return render(request, "register.html", context)

def editProfile(request, id):
    
    student = Student.objects.get(user_id=id) if Student.objects.filter(user_id=id).exists() else None
    user = User.objects.get(id=id)
    lecturers = Lecturer.objects.filter(user__is_active=1)
    context = {
        "name": user.full_name,
        "lecturers": lecturers,
        "student": student,
    }
    

    if request.method == 'POST':
        student = Student.objects.get(user_id=id)
        student.user = user
        student.matric_no = request.POST['matric'].upper()
        student.program = request.POST['program']
        # student.enrol_year = datetime.strptime(request.POST['enrol'], '%Y-%m').date()
        # student.grad_year = datetime.strptime(request.POST['grad'], '%Y-%m').date()
        enrol_sem = Semester.objects.filter(academic_year=request.POST['enrol_year'], semester=request.POST['enrol_sem']).first()
        grad_sem = Semester.objects.filter(academic_year=request.POST['grad_year'], semester=request.POST['grad_sem']).first()
        if not enrol_sem:
            enrol_sem = Semester()
            enrol_sem.academic_year = request.POST['enrol_year']
            enrol_sem.semester = request.POST['enrol_sem']
            enrol_sem.save()
        if not grad_sem:
            grad_sem = Semester()
            grad_sem.academic_year = request.POST['grad_year']
            grad_sem.semester = request.POST['grad_sem']
            grad_sem.save()
        student.lecturer_id = request.POST['lecturer']
        student.enrol_sem = enrol_sem
        student.grad_sem = grad_sem
        student.save()
        user = User.objects.get(id=id)
        user.full_name = request.POST['name'].upper()
        user.contact = request.POST['contact']
        user.address = request.POST['address']
        user.save()

   
        messages.success(request, "Your profile is updated.")
        return redirect('dashboard')
        
    return render(request, "edit_profile.html", context)

def manageStudent (request):
    students = Student.objects.all()
    semesters = Semester.objects.all()
    for semester in semesters:
        start = semester.start
        end = semester.end
        students = Student.objects.filter(enrol_year__range=(start,end))
        for student in students:
            student.enrol_sem = semester
            if student.program == '1':
                grad_year = int(semester.academic_year.split('/')[0]) + 3
                grad_year = str(grad_year) + '/' + f'{grad_year+1}'[2:]
                grad_sem = semester.semester
                
            elif student.program == '2' or student.program == '3':
                grad_year = int(semester.academic_year.split('/')[0]) + 1
                grad_year = str(grad_year) + '/' + f'{grad_year+1}'[2:]
                grad_sem = 2 if semester.semester == 1 else 1
            else:
                grad_year = int(semester.academic_year.split('/')[0]) + 2
                grad_year = str(grad_year) + '/' + f'{grad_year+1}'[2:]
                grad_sem = 2 if semester.semester == 1 else 1

            student.grad_sem = Semester.objects.filter(academic_year=grad_year, semester=grad_sem)
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

def printAllView (request):
    academic_years = Semester.objects.values('academic_year').distinct().order_by('academic_year')
    context = {
        "academic_years": academic_years
    }
    if 'print_all' in request.POST:
        semester = Semester.objects.filter(academic_year=request.POST['academic_year'], semester=request.POST['semester'])
        if semester:
            semester_id = semester.first().id
            print(semester_id)
            return redirect("download-all-transcripts", semester_id)
        else:
            messages.error(request, "Selected semester is not available. Please try other semesters.")
        
        return redirect ("print-all-transcripts")
    return render (request, "print_all_transcripts.html", context)
@login_required
def generateTranscriptView(request, user_id):
    current_date = datetime.now().date()
    current_year = Semester.objects.filter(end__gte=current_date, start__lte=current_date).first()
    student = ""

    if Student.objects.filter(user_id=user_id).exists():
        student = Student.objects.get(user_id=user_id) 

        # Event Participation
        event_pars_in = Event_Participants.objects.filter(student=student, attendance=1, event__internal=1).order_by('event__type')
        event_pars_ex = Event_Participants.objects.filter(student=student, attendance=1, event__internal=0).order_by('event__type')
        arts = Article.objects.filter(student=student, status=1, published__isnull=False)
        awarded_arts = Article.objects.filter(published__isnull=True)
        
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
            "event_in_post": event_pars_in.filter(event__type__in=[1,2,3,4]),
            "event_ex_post": event_pars_ex.filter(event__type__in=[1,2]),
            "event_in_others": event_pars_in.exclude(event__type__in=[1,2,3,4]),
            "event_ex_others": event_pars_ex.exclude(event__type__in=[1,2]),
            "org_coms_in": org_coms_in,
            "org_coms_ex": org_coms_ex,
            "total_in_length": total_in_length,
            "total_ex_length": total_ex_length,
            "arts": arts,
            "awarded_arts": awarded_arts,
            "other": other,
            "transcript": True,
            "hod_name": hod_name,
            "current": current_year,
        }

    else:
        context = {
            "transcript": False,
            "current": current_year,
        }
    if request.method == 'POST':
        
        if 'search' in request.POST:
            if Student.objects.filter(matric_no=request.POST['matric'].upper()).exists():
                student = Student.objects.get(matric_no=request.POST['matric'].upper())
                user_id = student.user_id
                return redirect ("generate-transcript", user_id=user_id)
            
            else:
                messages.error(request, "Student does not exists. Please enter a valid matric number.")
                return redirect ("generate-transcript", user_id=request.user.id)

            
        
    if not student:
        return render (request,"transcript_undergrad.html", context)
    elif student.program == 1:
        return render (request,"transcript_undergrad.html", context)
    else:
        return render (request,"transcript_postgrad.html", context)


   
@login_required
def dashboardView(request):
    current_date = datetime.now().date()
    if request.user.role in 'SUPER ADMIN':
    
        year_list = list()
        par_list = list()

        years = Semester.objects.values('academic_year').distinct().order_by('academic_year')

        
        current_year = Semester.objects.filter(end__gte=current_date, start__lte=current_date).first()
        selected_year = current_year
        event_selection = Events.objects.values('e_name').distinct()
        event_name = Events.objects.all().first().e_name
        upcoming_events = Events.objects.filter(start__gte=current_year.start)
        selected = event_name
        events = Events.objects.filter(e_name=event_name)
        upcoming_events = Events.objects.filter(start__gte=current_date).order_by("start")[:2]
        announcements = Announcement.objects.order_by("-created_time")[:2]
        num_active = Student.objects.filter(user__is_active=1).count()
        num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
        num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end).count()
        study_level = 1
        
        if request.method == 'POST':
            print(request.POST)
            # if 'event_name' in request.POST:
            #     events = Events.objects.filter(e_name=request.POST['event_name']).order_by("year")
            #     event_name = request.POST['event_name']
            #     selected = event_name

            

            if 'academic_year' in request.POST or 'semester' in request.POST or 'study_level' in request.POST:
                study_level = request.POST['study_level']
                if Semester.objects.filter(academic_year=request.POST['academic_year'], semester=request.POST['semester']).exists():
                    selected_year = Semester.objects.get(academic_year=request.POST['academic_year'], semester=request.POST['semester'])
                    
                else:
                    selected_year = Semester.objects.get(academic_year=request.POST['academic_year'])

                print(selected_year)

                if study_level == 'All':
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end).count()
                elif study_level == '1':
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end,student__program=1).count()
                elif study_level == '2':
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end,student__program=2).count()
                elif study_level == '3':
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end,student__program=3).count()
                elif study_level == '4':
                    num_event = Events.objects.filter(start__gte=selected_year.start, end__lte=selected_year.end).count()
                    num_article = Article.objects.filter(date__gte=selected_year.start, date__lte=selected_year.end,student__program=4).count()
                

                if selected_year == current_year:
                    active = Student.objects.filter(user__is_active=1)
                    if study_level == 'All':
                        num_active = active.count()
                    elif study_level== '1':
                        num_active = active.filter(program=1).count()
                    elif study_level == '2':
                        num_active = active.filter(program=2).count()
                    elif study_level == '3':
                        num_active = active.filter(program=3).count()
                    elif study_level == '4':
                        num_active = active.filter(program=4).count()
                else:
                    students = Student.objects.filter(grad_sem__end__gte=selected_year.start, enrol_sem__start__lte=selected_year.start)
                    
                    if study_level == 'All':
                        num_active = students.count()
                    elif study_level == '1':
                        num_active = students.filter(program=1).count()
                    elif study_level == '2':
                        num_active = students.filter(program=2).count()
                    elif study_level == '3':
                        num_active = students.filter(program=3).count()  
                    elif study_level == '4':
                        num_active = students.filter(program=4).count()                  
           
            
        # for event in events:
        #     year_list.append(event.year)
        #     number = Event_Participants.objects.filter(event=event, attendance=1).count()
        #     par_list.append(number) 

       
        df_students = pd.DataFrame(columns=["enrol_sem", "program", "count"])
        semesters = Semester.objects.all()
        for semester in semesters:
            enrol_sem = str(semester.academic_year) + " Sem " + str(semester.semester)
            student_count = Student.objects.filter(enrol_sem=semester).count()
            undergrad_count = Student.objects.filter(enrol_sem=semester, program=1).count()
            postgrad_count = Student.objects.filter(enrol_sem=semester, program__in=[2,3,4]).count()
            df_students.loc[len(df_students.index)] = [enrol_sem, "All", student_count]
            df_students.loc[len(df_students.index)] = [enrol_sem, "Undergraduate", undergrad_count]
            df_students.loc[len(df_students.index)] = [enrol_sem, "Postgraduate", postgrad_count] 

        df_students = df_students.sort_values(by=['enrol_sem'])  
        print(df_students)

        fig = px.line(df_students, x='enrol_sem', y='count', color='program', line_group='program',
              labels={'count': 'Number of Students', 'enrol_sem': 'Year and Semester'},
              title='Number of Students Enrolled in Each Semester by Study Level',
              )
        
        # par_df = pd.DataFrame({'Year':year_list, 'Participants': par_list})
        # fig = px.line(par_df, x="Year", y="Participants", title=f'Number of Participants for {event_name}')
        # fig.update_traces(mode="lines+markers")
        # fig.update_xaxes(tickvals=year_list)
        # fig.update_yaxes(dtick=1)
        fig.update_xaxes(rangeslider_visible=True)
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
        pd_count = Event_Participants.objects.filter(student=student, event__type=3, attendance=1).count()
        cd_count = Event_Participants.objects.filter(student=student, event__type=4, attendance=1).count()
        conf_count = Event_Participants.objects.filter(student=student, event__type=2, attendance=1).count()
        seminar_count = Event_Participants.objects.filter(student=student, event__type=1, attendance=1).count()
        pd_cd_count = pd_count + cd_count
        context = { 
            "student": student,
            "announcements": announcements,
            "registered_events": registered_events,
            "par_count": par_count,
            "com_count": com_count,
            "org_count": org_count,
            "art_count": art_count,
            "pd_count": pd_count,
            "cd_count": cd_count,
            "conf_count": conf_count,
            "seminar_count": seminar_count,
            "pd_cd_count": pd_cd_count,
        }
        return render(request, "dashboard_student.html", context)
    
    else:
        lecturer = Lecturer.objects.get(user=request.user)
        print(lecturer)
        students = Student.objects.filter(lecturer=lecturer)
        undergrad_students = students.filter(program=1)
        master_cw = students.filter(program=2)
        master_re = students.filter(program=3)
        phd_students = students.filter(program=4)
        print("students: ",students)
        context = {
            "lecturer": lecturer,
            "students": students,
            "active_student": len(students),
            "undergrad": len(undergrad_students),
            "master_cw": len(master_cw),
            "master_re": len(master_re),
            "phd": len(phd_students),
        }
        return render (request, "dashboard_lecturer.html", context)
    
def postgradDetailsView (request):
    selected_program = ""
    if "HEAD OF DEPARTMENT" in request.user.role or "ADMIN" in request.user.role:
        print("HOD OR ADMIN")
        students = Student.objects.filter(program__in=[2,3,4], user__is_active=1)
    elif "LECTURER" in request.user.role:
        print("LECTURER")
        lecturer = Lecturer.objects.get(user=request.user)
        students = Student.objects.exclude(program='1', user__is_active=0).filter(lecturer=lecturer)

    if request.method == 'POST':
        if 'program' in request.POST:
            selected_program = request.POST['program']
            if not 'all' in request.POST['program']:
                students = students.filter(program=request.POST['program'])
        if 'submit-dates' in request.POST:
            print(request.POST)
            rm_date  = datetime.strptime(request.POST['rm_date'], "%Y-%m-%dT%H:%M") if request.POST['rm_date'] != "" else None
            pd_date  = datetime.strptime(request.POST['pd_date'], "%Y-%m-%dT%H:%M") if request.POST['pd_date'] != "" else None
            cd_date  = datetime.strptime(request.POST['cd_date'], "%Y-%m-%dT%H:%M") if request.POST['cd_date'] != "" else None
            viva_date  = datetime.strptime(request.POST['viva_date'], "%Y-%m-%dT%H:%M") if request.POST['viva_date'] != "" else None
            student = Student.objects.get(id=request.POST['submit-dates'])
            student.rm_date = rm_date 
            student.pd_date = pd_date
            student.cd_date = cd_date
            student.viva_date = viva_date
            if 'rm' in request.POST:
                student.rm_status = 1
            else:
                student.rm_status = 0
            if 'pd' in request.POST:
                student.pd_status = 1
            else:
                student.pd_status = 0
            if 'cd' in request.POST:
                student.cd_status = 1
            else:
                student.cd_status = 0
            if 'viva' in request.POST:
                student.viva_status = 1
            else:
                student.viva_status = 0
            student.save()
            return redirect ("postgrad")
    context = {
        "students": students,
        "program_opt": Student.program.field.choices,
        "selected_program": selected_program,
    }
    return render (request, "postgrad_details.html", context)

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

def graduateReportView (request):
    semester_years = Semester.objects.values('academic_year').distinct().order_by("academic_year")
    students = None
    selected_sem = None

    if request.method == 'POST':
        academic_year = request.POST['academic_year']
        semester = request.POST['semester']
        if Semester.objects.filter(academic_year=academic_year, semester=semester).exists():
            selected_sem = Semester.objects.get(academic_year=academic_year, semester=semester)
            students = Student.objects.filter(grad_sem=selected_sem)

        else:
            messages.error(request, f"No record for Year {academic_year} Semester {semester}.")
            return redirect("graduate-report")
        
    context = {
        "semester_years": semester_years,
        "students": students,
        "selected_sem": selected_sem,
        "graduate": 1,
    }

    return render (request, "graduate_report.html",context)

def activeReportView (request):
    semester_years = Semester.objects.values('academic_year').distinct().order_by("academic_year")
    students = None
    selected_sem = None

    if request.method == 'POST':
        academic_year = request.POST['academic_year']
        semester = request.POST['semester']
        if Semester.objects.filter(academic_year=academic_year, semester=semester).exists():
            selected_sem = Semester.objects.get(academic_year=academic_year, semester=semester)
            students = Student.objects.filter(enrol_year__lte=selected_sem.start, grad_year__gte=selected_sem.end)
            
        else:
            messages.error(request, f"No record for Year {academic_year} Semester {semester}.")
            return redirect("active-report")
        
    context = {
        "semester_years": semester_years,
        "students": students,
        "selected_sem": selected_sem,
        "active": 1,
    }
    return render (request, "graduate_report.html",context)
    
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
            'student_lect': student.lecturer_id,
            'rm_date': student.rm_date,
            'pd_date': student.pd_date,
            'cd_date': student.cd_date,
            'viva_date': student.viva_date,
            'rm': student.rm_status,
            'pd': student.pd_status,
            'cd': student.cd_status,
            'viva': student.viva_status,
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