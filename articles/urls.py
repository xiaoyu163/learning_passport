from django.urls import path

from . import views
urlpatterns = [
    path('upload/event', views.uploadEventView, name="upload-event"),
    path('upload/org', views.uploadOrgView, name="upload-org"),
    path('upload/article', views.uploadArticleView, name="upload-article"),
    path('verify/event', views.verEventView, name="verify-event"),
    path('verify/org', views.verOrgView, name="verify-org"),
    path('verify/article', views.verArtView, name="verify-article"),
    path('status', views.statusView, name="status"),
    path('download/<str:template_name>', views.download_excel, name='download_excel'),
]