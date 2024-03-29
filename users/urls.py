from django.urls import path

from . import views

from django.contrib.auth import views as auth_views
 

from users.views import ResetPasswordView
 
urlpatterns = [
    path('', views.dashboardView, name="dashboard"),
    path('login', views.loginView, name="login"),
    path('logout', views.logoutView, name="logout"),
    path('register', views.registerView, name="register"),
    path('edit-profile/<str:id>', views.editProfile, name="edit-profile"),
    path('manage-student', views.manageStudent, name="manage-student"),
    path('manage-lecturer', views.manageLecturer, name="manage-lecturer"),
    path('change-password', views.resetPasswordView, name="change-password"),
    path('password-reset', ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
     path('generate_transcript/<int:user_id>/', views.generateTranscriptView, name="generate-transcript"),
     path('get-student-details/<int:student_id>/', views.get_student_details, name='get-student-details'),
     path('get-lecturer-details/<int:lecturer_id>/', views.get_lecturer_details, name='get-lecturer-details'),
     path('get-semester-details/<int:semester_id>/', views.get_semester_details, name='get-semester-details'),
     path('semester-dates', views.semesterDatesView, name="semesters"),
     path('graduate-report', views.graduateReportView, name="graduate-report"),
     path('inquiry', views.inquiryView, name="inquiry"),
     path('active-report', views.activeReportView, name="active-report"),
     path('postgrad', views.postgradDetailsView, name="postgrad"),
     path('generate-pdf/<int:student_id>', views.generatePDF, name="generate-pdf"),
     path('download-all-transcripts/<int:semester_id>', views.download_all_transcripts, name='download-all-transcripts'),
     path('print-all-transcripts', views.printAllView, name="print-all-transcripts")
]