from django import template
from datetime import timedelta
from django.utils import timezone



register = template.Library()


@register.filter()
def pretty_date(value):
    print("custom_filters loaded")
    if value:
        today = timezone.now().date()
        value = timezone.localtime(value)

        if value.date() == today:
            return f"Today at {value.strftime('%B %d, %Y at %I:%M %p')}"
        if value.date() == today-timedelta(days=1):
            return f"Yesterday at {value.strftime('%B %d, %Y at %I:%M %p')}" #strftime
        else:
            return f"{value.strftime('%B %d, %Y at %I:%M %p')}"
    
    return "No login record"