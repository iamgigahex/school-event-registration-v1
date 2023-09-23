from django.db import models

# Create your models here.
from django.urls import reverse


class Events(models.Model):
    """
    Holds Events related details.
    """
    event_name = models.CharField(max_length=255)
    event_date_time = models.DateTimeField()
    event_location = models.CharField(max_length=255)
    event_description = models.TextField()
    max_participants = models.PositiveIntegerField()

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])


class Participant(models.Model):
    """
    Holds Participant related details.
    """
    first_name = models.CharField(null=False, max_length=60, verbose_name='First Name')
    last_name = models.CharField(null=False, max_length=60, verbose_name='Last Name')
    phone_number = models.CharField(null=False, max_length=60, verbose_name='Phone Number')
    email = models.EmailField(unique=True, verbose_name='Email')
    profile_picture = models.ImageField(upload_to='profile_images/', verbose_name='Profile Picture', blank=True,
                                        null=True)
    events = models.ManyToManyField(Events, related_name='events_participants', blank=True)

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_events_list(self):
        return self.events.all().values_list('name', flat=True)

    def __repr__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'
