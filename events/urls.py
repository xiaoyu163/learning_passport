from django.urls import path

from . import views
urlpatterns = [
    path('events', views.eventListView, name="events"),
    path('events/<int:id>', views.eventDetailView, name="event-detail"),
    path('events/attendance', views.takeAttendanceView, name="attendance"),
    path('event/admin-attendance/<int:event_id>', views.adminAttendaceView, name="admin-attendance"),
    path('get-event-details/<int:event_id>', views.get_event_details, name='get_event_details'),
    path('announcements', views.announcementListView, name="announcements"),
    path('get-ann-details/<int:ann_id>/', views.get_ann_details, name='get_ann_details'),

]