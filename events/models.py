from django.db import models
from django.utils import timezone   # <-- Use timezone instead of datetime



class Event(models.Model):
    eventName = models.CharField(max_length=100, null=False, blank=False)
    eventDate = models.DateField(default=timezone.localdate)   # Correct
    eventTime = models.TimeField(default=timezone.now)   # Correct
    eventLocation = models.TextField(max_length=100, null=False, blank=False)
    eventImage = models.ImageField(upload_to='events_photo', default='events_photo/defaultevent.png', blank=True, null=True)

    catagory = models.ForeignKey(
        "Catagory",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="event_catagory"
    )

    #users:
    participants = models.ManyToManyField(
        "users.Participant",
        related_name="rsvp_events", # event_participant
        blank=True
    )

    def __str__(self):
        return self.eventName




class Catagory(models.Model):
    catagoryName = models.CharField(max_length=100)
    catagoryDescription = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.catagoryName







""" 

widgets = {
    "participants": forms.CheckboxSelectMultiple(),
    "catagory": forms.Select(),
    "eventDate": forms.SelectDateWidget(),
    "eventTime": forms.TimeInput(attrs={'type': 'time'}),
}


 """
