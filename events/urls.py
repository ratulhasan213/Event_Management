from django.urls import path
from django.urls import path
from events.views import dashboard,create_event,create_catagory,create_participant,details,editEvent,deleteEvent,editParticipant,deleteParticipant,editCatagory,deleteCatagory

urlpatterns = [
    path('dashboard/',dashboard,name="dashboard"),
    path("create_event/",create_event,name = "create_event"),
    path("create_catagory/",create_catagory,name = "create_catagory"),
    path("create_participant/",create_participant,name = "create_participant"),
    path("details/<int:eventID>/",details,name = "details"),
    path("editEvent/<int:eventID>/",editEvent,name = "editEvent"),
    path("deleteEvent/<int:eventID>/",deleteEvent,name = "deleteEvent"),
    path("editParticipant/<int:participantID>/",editParticipant,name = "editParticipant"),
    path("deleteParticipant/<int:participantID>/",deleteParticipant,name = "deleteParticipant"),
    path("editCatagory/<int:catagoryID>/",editCatagory,name = "editCatagory"),
    path("deleteCatagory/<int:catagoryID>/",deleteCatagory,name = "deleteCatagory")
]
