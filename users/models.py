from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Participant(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='participant'
    )

    participantPhoto = models.ImageField(upload_to='participants_photo', default='participants_photo/defaultparticipant.png', blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True)
    def __str__(self):
        return self.user.username