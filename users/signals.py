from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.urls import reverse
from users.models import Participant





@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        relative_url = reverse('users:activate_user', kwargs={'user_id': instance.id, 'token': token})
        activation_url = f"{settings.FRONT_END_URL}{relative_url}"
        message =  f"Hi {instance.username}. Please activate your account.\n {activation_url} \nThank you"

        try:
            send_mail(
                subject="Activation Email",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
            )
        except Exception as e:
            print(f"failed to send email: {instance.email}. Error: {str(e)}")



@receiver(post_save,sender=User)
def create_participant(sender,instance,created,**kwargs):
    if created:
        Participant.objects.create(user = instance)