from django.urls import path
from django.urls import path
from events.views import no_permission
from events.views import DashBoard,Details,CreateEvent,EditEvent,DeleteEvent,CreateCatagory,EditCatagory,RSVP,DeleteCatagory
app_name = 'events'


urlpatterns = [
    path('dashboard/',DashBoard.as_view(),name="dashboard"),
    path("create_event/",CreateEvent.as_view(),name = "create_event"),
    path("create_catagory/",CreateCatagory.as_view(),name = "create_catagory"),
    path("details/<int:eventID>/",Details.as_view(),name = "details"),
    path("editEvent/<int:eventID>/",EditEvent.as_view(),name = "editEvent"),
    path("deleteEvent/<int:eventID>/",DeleteEvent.as_view(),name = "deleteEvent"),
    path("editCatagory/<int:catagoryID>/",EditCatagory.as_view(),name = "editCatagory"),
    path("deleteCatagory/<int:catagoryID>/",DeleteCatagory.as_view(),name = "deleteCatagory"),
    path("rsvp/int<eventID>/",RSVP.as_view(),name = "rsvp"),
    path("no_permission/",no_permission, name = "no_permission"),
   
]
