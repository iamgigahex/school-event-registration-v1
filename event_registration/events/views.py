import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView

from events.forms import BulkUploadForm, ParticipantForm, EventForm
from events.models import Participant, Events
from events.utility import Utilities


class EventListView(ListView):
    model = Events
    form_class = BulkUploadForm
    extra_context = {
        'bulk_upload_form': form_class,
    }
    template_name = "event_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}
        event_date_search = self.request.GET.get('event_date', '').strip()
        event_search = self.request.GET.get('event_name', '').strip()

        # Check if event_date_search is provided and valid
        if event_date_search:
            try:
                event_date = datetime.datetime.strptime(event_date_search, '%Y-%m-%d')
                filter_params['event_date_time__date'] = event_date.date()
            except ValueError:
                pass

        # Check if event_search is provided
        if event_search:
            filter_params['event_name__icontains'] = event_search

        # Apply filtering
        if filter_params:
            queryset = queryset.filter(**filter_params)

        return queryset


class EventDetailsView(DetailView):
    model = Events
    template_name = "event_details.html"
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object  # Get the event instance from the view
        participants = event.events_participants.all()  # Get all participants for the event
        context['participants'] = participants
        return context


@method_decorator(login_required, name='dispatch')
class BulkUploadView(View):
    form_class = BulkUploadForm
    success_url = reverse_lazy('event_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        success, failed = Utilities.upload_from_csv(request.FILES['csv_file'], request.FILES['image_zipfile'])
        if success:
            messages.success(request, f'Successfully uploaded {success} entries')
        if failed:
            messages.error(request, f'Fail to upload {failed} entries')
        return HttpResponseRedirect(reverse_lazy('event_list'))


class AddParticipantToEventView(View):
    template_name = "add_participant.html"

    def get_form(self, request, event_id):
        return ParticipantForm()

    def get(self, request, event_id):
        event = get_object_or_404(Events, pk=event_id)
        form = form = ParticipantForm()
        return render(request, self.template_name, {'form': form, 'event': event})

    def post(self, request, event_id):
        event = get_object_or_404(Events, pk=event_id)
        form = ParticipantForm(request.POST, request.FILES)

        if form.is_valid():
            # Check if the maximum number of participants has been reached
            if event.events_participants.count() < event.max_participants:
                # Create a new participant
                participant = form.save(commit=False)
                participant.save()
                participant.events.add(event)  # Add the evFent to the participant's events

                # return redirect('event-details', event_id=event_id)
                return redirect(reverse_lazy('event-detail', kwargs={'pk': event_id}))
            else:
                # Maximum participants reached, display an error message
                form.add_error(None, 'Maximum number of participants reached for this event.')

        return render(request, self.template_name, {'form': form, 'event': event})


class EventCreateView(CreateView):
    model = Events
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_list')


class EventUpdateView(UpdateView):
    model = Events
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_list')
