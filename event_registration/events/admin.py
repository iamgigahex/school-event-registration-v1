from django.contrib import admin

from events.models import Events, Participant

# Register your models here.


admin.site.register(Events)
admin.site.register(Participant)
