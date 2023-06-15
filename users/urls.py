from django.urls import path

from . import views
urlpatterns = [
    path('', views.dashboardView, name="dashboard"),
    path('login', views.loginView, name="login"),
    path('logout', views.logoutView, name="logout"),
    path('register', views.registerView, name="register"),
    path('edit-profile/<str:id>', views.editProfile, name="edit-profile"),

]