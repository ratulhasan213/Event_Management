from django.urls import path
from django.urls import path

from users.views import sign_up,activate_user,log_in,log_out,edit_participant,delete_participant,participant_profile,assign_role,create_group,my_profile,change_role,superuser_profile

app_name = 'users'

urlpatterns = [
    path("sign_up/",sign_up,name ="sign_up"),
    path("activate_user/<int:user_id>/<str:token>/",activate_user,name = 'activate_user'),
    path('log_in/',log_in,name = 'log_in'),
    path("log_out/",log_out,name = "log_out"),
    path("editParticipant/<int:participantID>/",edit_participant,name = "edit_participant"),
    path("deleteParticipant/<int:participantID>/",delete_participant,name = "delete_participant"),
    path("participant_profile/<int:participantID>",participant_profile,name = "participant_profile"),
    path("profile/",my_profile, name="my_profile"),
    path("superuser_profile/",superuser_profile,name="superuser_profile"),
    path("assign_role/",assign_role,name = 'assign_role'),
    path("change_role/<int:participantID>/",change_role, name="change_role"),
    path("create_group/",create_group,name = 'create_group'),
]
