from django.db import models
from datetime import datetime

# Create your models here.


class Event(models.Model):
    eventName = models.CharField(max_length=100,null=False,blank=False)
    eventDate = models.DateField(default=datetime.now().date())
    eventTime = models.TimeField(default=datetime.now().time())
    eventLocation = models.TextField(max_length=100,null=False,blank=False)

    catagory = models.ForeignKey(
        "Catagory",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="event_catagory"
    )

    participants = models.ManyToManyField("Participant", related_name="event_participant")

    def __str__(self):
        return self.eventName


class Catagory(models.Model):
    catagoryName = models.CharField(max_length=100)
    catagoryDescription = models.TextField(null=False,blank=False)

    def __str__(self):
        return self.catagoryName

class Participant(models.Model):
    participantName = models.CharField(max_length=100,null=False,blank=False)
    participantEmail = models.EmailField(max_length=254,null=False,blank=False,unique=True)

    def __str__(self):
        return self.participantName


