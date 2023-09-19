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
    path('change-password', views.resetPasswordView, name="change-password"),
    path('password-reset', ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),


]