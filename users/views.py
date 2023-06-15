from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Student
from django.contrib.auth.hashers import make_password
from datetime import datetime

# Create your views here.


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

def dashboardView(request):
  
    return render(request, "dashboard.html")

@login_required
def logoutView(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect('login')

def registerView(request):
    if request.method == 'POST':
        print(request.POST)
        new_user = User()
        new_user.email = request.POST['email']
        new_user.password = make_password(request.POST['password'])
        new_user.role = request.POST['role']
        new_user.full_name = request.POST['name']

        if User.objects.filter(email=new_user.email):
            messages.info(request, "Account already exist. Please proceed to login.")
            return redirect('login')
        
        else:
            new_user.save()
            id = new_user.id       
        
            if new_user.role not in 'STUDENT':
                messages.success(request,"Your account is registered successfully. Please proceed to login.")
                return redirect('login')
            
            else:
                return redirect('edit-profile', id=id)
    
    return render(request, "register.html")

def editProfile(request, id):
    user = User.objects.get(id=id)
    context = {
        "matric": user.email.split('@')[0],
        "name": user.full_name,
    }
    

    if request.method == 'POST':
        student = Student()
        student.user = user
        student.matric_no = request.POST['matric']
        student.program = request.POST['program']
        student.enrol_year = datetime.strptime(request.POST['enrol'], '%Y-%m').date()
        student.grad_year = datetime.strptime(request.POST['grad'], '%Y-%m').date()
        student.save()
        user = User.objects.get(id=id)
        user.full_name = request.POST['name']
        user.contact = request.POST['contact']
        user.address = request.POST['address']
        user.save()

        messages.success(request,"Your account is registered successfully. Please proceed to login.")
        return redirect('login')
        
    return render(request, "edit_profile.html", context)

