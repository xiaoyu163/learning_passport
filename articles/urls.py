from django.urls import path

from . import views
urlpatterns = [
    path('uploads', views.uploadsView, name="uploads"),
    path('download/<str:template_name>', views.download_excel, name='download_excel'),
]