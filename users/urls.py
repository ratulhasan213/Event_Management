from django.urls import path
from django.urls import path

from users.views import SingUpView,ParticipantProfile,MyProfile,EditParticipant,ActivateUser,Login,LogOut,DeleteParticipant,AssignRole,ChangeRole,CreateGroup,ChangePassword,ChangePasswordDone


app_name = 'users'

urlpatterns = [
    path("sign_up/",SingUpView.as_view(),name ="sign_up"),
    path("activate_user/<int:user_id>/<str:token>/",ActivateUser.as_view(),name = 'activate_user'),
    path('log_in/',Login.as_view(),name = 'log_in'),
    path("log_out/",LogOut.as_view(),name = "log_out"),
    path("editParticipant/<int:participantID>/",EditParticipant.as_view(),name = "edit_participant"),
    path("deleteParticipant/<int:participantID>/",DeleteParticipant.as_view(),name = "delete_participant"),
    path("participant_profile/<int:participantID>",ParticipantProfile.as_view(),name = "participant_profile"),
    path("profile/",MyProfile.as_view(), name="my_profile"),
    path("assign_role/",AssignRole.as_view(),name = 'assign_role'),
    path("change_role/<int:participantID>/",ChangeRole.as_view(), name="change_role"),
    path("create_group/",CreateGroup.as_view(),name = 'create_group'),
    path("change_password/",ChangePassword.as_view(),name = 'change_password'),
    path('password_change_done/',ChangePasswordDone.as_view(),name = 'password_change_done'),

    #ResetPassword,PasswordResetConfirm,PasswordResetDoneView:This is written in the projec urls due to app the name.
  


      # path("participant_profile/<int:participantID>",participant_profile,name = "participant_profile"),
      #path("profile/",my_profile, name="my_profile"),
      #path("editParticipant/<int:participantID>/",edit_participant,name = "edit_participant"),
      # path("sign_up/",sign_up,name ="sign_up"),
      # path("activate_user/<int:user_id>/<str:token>/",activate_user,name = 'activate_user'),
      #path('log_in/',log_in,name = 'log_in'),
      #path("log_out/",log_out,name = "log_out"),
      #path("deleteParticipant/<int:participantID>/",delete_participant,name = "delete_participant"),
      #path("assign_role/",assign_role,name = 'assign_role'),
      #path("change_role/<int:participantID>/",change_role, name="change_role"),
      #path("create_group/",create_group,name = 'create_group'),
]
