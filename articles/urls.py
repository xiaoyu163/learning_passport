from django.urls import path

from . import views
urlpatterns = [
    path('submit/event', views.submitEventView, name="submit-event"),
    path('submit/event/form', views.eventComFormView, name="event-com-form"),
    path('submit/event/form/<int:form_id>', views.editEventComView, name="edit-event-com-form"),
    path('submit/org', views.submitOrgView, name="submit-org"),
    path('submit/article', views.submitArticleView, name="submit-article"),
    path('verify/event', views.verEventView, name="verify-event"),
    path('verify/org', views.verOrgView, name="verify-org"),
    path('verify/article', views.verArtView, name="verify-article"),
    path('status', views.statusView, name="status"),
    path('download/<str:template_name>', views.download_excel, name='download_excel'),

]