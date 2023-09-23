"""
Events  URL configuration.
"""
from django.urls import path
from .views import EventListView, EventDetailsView, BulkUploadView, AddParticipantToEventView, EventCreateView, \
    EventUpdateView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('detail/<int:pk>/', EventDetailsView.as_view(), name='event-detail'),
    path('bulk_upload', BulkUploadView.as_view(), name='bulk_upload'),
    path('events/<int:event_id>/add-participant/', AddParticipantToEventView.as_view(), name='add_participant'),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),


]