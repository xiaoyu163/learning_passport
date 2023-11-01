from django.urls import path

from . import views
urlpatterns = [
    path('uplaod/event', views.submitEventView, name="upload-event"),
    # path('submit/event', views.submitEventView, name="submit-event"),
    # path('submit/event/form', views.eventComFormView, name="event-com-form"),
    # path('submit/event/form/<int:form_id>', views.editEventComView, name="edit-event-com-form"),
    path('upload/org', views.submitOrgView, name="upload-org"),
    path('upload/article', views.submitArticleView, name="upload-article"),
    path('upload/other', views.submitOtherComp, name="upload-other"),
    path('verify/event', views.verEventView, name="verify-event"),
    path('verify/org', views.verOrgView, name="verify-org"),
    path('verify/article', views.verArtView, name="verify-article"),
    path('verify/other', views.verOtherView, name="verify-other"),
    path('status', views.statusView, name="status"),
    path('download/<str:template_name>', views.download_excel, name='download_excel'),
    path('get-art-details/<int:art_id>/', views.get_art_details, name='get-art-details'),
    path('get-internal-com-details/<int:event_id>/', views.get_internal_com_details, name='get-internal-com-details'),
    path('get-external-com-details/<int:com_id>/', views.get_external_com_details, name='get-external-com-details'),
    path('get-internal-org-details/<int:org_id>/', views.get_internal_org_details, name='get-internal-org-details'),
    path('get-external-org-details/<int:org_com_id>/', views.get_external_org_details, name='get-external-org-details'),   
    path('get-other-comp-details/<int:comp_id>/', views.get_other_comp_details, name='get-other-comp-details'),   
]