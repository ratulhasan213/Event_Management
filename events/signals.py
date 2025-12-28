from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from users.models import Participant
from django.conf import settings




@receiver(m2m_changed,sender=Event.participants.through)
def send_rsvp_email(sender,instance,action,pk_set,**kwargs):
    if action == "POST":
        try:
            p_id = list(pk_set)[0]
            participant = Participant.objects.select_related("user").get(id=p_id)
            user = participant.user
            message = f"Hi {user.username},\n\nThank you for participating in {instance.eventName}!"
            
            send_mail(
                    subject=f"Thank you for RSVPing to {instance.eventName}",
                    message=message,
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
        except Exception as e:
            print(f"failed to send email. Error: {str(e)}")
