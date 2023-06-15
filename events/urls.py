from django.urls import path

from . import views
urlpatterns = [
    path('events', views.eventListView, name="events"),
    path('events/<int:id>', views.eventDetailView, name="events"),
    path('events/registered', views.eventRegisteredView, name="registered"),
    path('get-event-details/<int:event_id>/', views.get_event_details, name='get_event_details')
]   