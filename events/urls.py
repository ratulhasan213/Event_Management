from django.urls import path
from django.urls import path
from events.views import dashboard,create_event,create_catagory,details,editEvent,deleteEvent,editCatagory,deleteCatagory,rsvp,no_permission

app_name = 'events'


urlpatterns = [
    path('dashboard/',dashboard,name="dashboard"),
    path("create_event/",create_event,name = "create_event"),
    path("create_catagory/",create_catagory,name = "create_catagory"),
    path("details/<int:eventID>/",details,name = "details"),
    path("editEvent/<int:eventID>/",editEvent,name = "editEvent"),
    path("deleteEvent/<int:eventID>/",deleteEvent,name = "deleteEvent"),
    path("editCatagory/<int:catagoryID>/",editCatagory,name = "editCatagory"),
    path("deleteCatagory/<int:catagoryID>/",deleteCatagory,name = "deleteCatagory"),
    path("rsvp/int<eventID>/",rsvp,name = "rsvp"),
    path("no_permission/",no_permission, name = "no_permission"),
   
]
