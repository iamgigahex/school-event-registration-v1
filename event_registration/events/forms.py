from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms

from events.models import Participant, Events


class BulkUploadForm(forms.Form):
    """BulkUpload Form """
    csv_file = forms.FileField(label="Event's CSV file ",
                               widget=forms.FileInput(attrs={'accept': '.csv', 'class': 'form-control'}))
    image_zipfile = forms.FileField(label="Zipfile with images",
                                    widget=forms.FileInput(attrs={'accept': '.zip', 'class': 'form-control'}))


class ParticipantForm(forms.ModelForm):
    """Participant Form"""

    class Meta:
        model = Participant
        fields = ['first_name',
                  'last_name',
                  'profile_picture',
                  'email',
                  'phone_number',
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False  # Profile picture is optional


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'


