from django.shortcuts import render,redirect
from users.forms import UserForm,ParticipantModelForm,LoginForm,UserEditForm,AssignRoleForm,CreateGroupForm,ChangeRoleForm
from users.models import Participant

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import  permission_required,user_passes_test

# Create your views here.



def get_user_role(user):
    role = None

    if user.is_superuser:
        role = "Admin"
    else:
        group = user.groups.first()
        if group:
            role = group.name
        else:
            role = "Member"

    return role


def can_assign_change_role(user):
    return get_user_role(user) == "Admin"




def sign_up (request): #create_participant
   

   user_form = UserForm()    
   participant_form = ParticipantModelForm()
   
   if request.method == "POST":
       user_form = UserForm(request.POST)
       participant_form = ParticipantModelForm(request.POST,request.FILES)
       if user_form.is_valid() and participant_form.is_valid():
           
           user = user_form.save(commit=False)
           user.set_password(user_form.cleaned_data.get('password'))
           user.is_active = False
           user.save()
           participant = participant_form.save(commit=False)
           participant.user = user
           participant.save()
           messages.success(request,"Memebership Created Successfully.Please check your email")
           return redirect("users:sign_up") #create_participant
       
   
   context = {
       "user_form":user_form,
       "participant_form":participant_form
   }
        
   
   return render(request,"sign_up.html",context)



#no need of decorator here yet..
def activate_user(request,user_id,token):

    status = ""
   
    try:
        user = User.objects.get(id =user_id)
        if default_token_generator.check_token(user,token):
               
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    status = "activated"
                else:
                    status = "alreadyActivated"
                
        else:
                 status = "invalid"

        context = {
            "status":status    
                   }
        
        return render(request,"user_activation.html",context)
        
    except User.DoesNotExist:
        return HttpResponse("user deos not exist")



def log_in(request):
    login_form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request,data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request,user)
            if request.user.is_superuser:
                return redirect("events:dashboard")
            else:
             return redirect("users:my_profile")
    
    context = {"login_form": login_form}
    
    return render(request,"log_in.html",context)


#no decorator: force the un-authenticate user to go into login page . even if anyhone hits the url manually: http://127.0.0.1:8000/users/log_out/
def log_out(request):
        if request.user.is_authenticated:
            messages.success(request,f"{request.user.username} logged out successfully")
            logout(request)
            
        else:
            messages.warning(request,"please Login first")
        
        return redirect('users:log_in')



#authentication check enough:
def my_profile(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request,"please Login first")
        return redirect("users:log_in")
    
    if user.is_superuser:
        return redirect("users:superuser_profile")
    participant = getattr(request.user,'participant',None)
    return redirect(
        "users:participant_profile",
        participant.id
    )


#authentication check enough:
def superuser_profile(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request,"please Login first")
        return redirect("users:log_in")

    if not user.is_superuser:
        return redirect("users:my_profile")

    return render(
        request,
        "superuser_profile.html",
        {"user": request.user}
    )




#authentication check enough:
def participant_profile(request,participantID):

    viewer = request.user
    if not viewer.is_authenticated:
        messages.warning(request,"please Login first")
        return redirect("users:log_in")

    viewer_participant = getattr(viewer,'participant',None)



    participant = Participant.objects.select_related("user").get( id =  participantID)

    events = participant.rsvp_events.all()
    participant_role = get_user_role(participant.user)
    change_role_form = ChangeRoleForm()
    viewer_role = get_user_role(request.user)

    can_view_form = (viewer.is_superuser or 
                     (participant_role!="Admin" and viewer.groups.filter(name = "Admin").exists())
                    )

    context = {
        "participant": participant,
        "viewer_role": viewer_role,
        "participant_role":participant_role,
        "events": events,
        "change_role_form":change_role_form,
        "can_view_form":can_view_form
    }

    return render(request, "participant_profile.html", context)







@permission_required("auth.change_user",login_url="events:no_permission")
def edit_participant(request,participantID):
  
  participant = Participant.objects.get(id = participantID)
  participant_form = ParticipantModelForm(instance = participant)
  user = participant.user
  user_form = UserEditForm(instance = user)


  if request.method == "POST":
      participant_form = ParticipantModelForm(request.POST, request.FILES, instance = participant)
      user_form = UserEditForm(request.POST,instance = user)
      if participant_form.is_valid() and user_form.is_valid():
          user_form.save()
          participant_form.save()
          messages.success(request,"Member Edited Successfully")
          return redirect("events:dashboard")
    
      else:
        messages.error(request,"Something Went Wrong")
        return redirect("events:dashboard")

  context = {
        "user_form":user_form,
        "participant_form":participant_form
    }
  
  return render(request,"sign_up.html",context)




@permission_required("auth.delete_user",login_url="events:no_permission")
def delete_participant(request, participantID):

    if request.method == "POST":
        participant = Participant.objects.get(id = participantID)
        name = participant.user.username
        participant.user.delete()
        messages.success(request,f"{name} Deleted Successfully")
       
    
    else:
        messages.error(request,"Something Went Wrong")
    
    return redirect("events:dashboard")





@user_passes_test(can_assign_change_role,login_url="events:no_permission")
def assign_role(request):
    assign_role_form = AssignRoleForm()

    if request.method == 'POST':
        assign_role_form = AssignRoleForm(request.POST)
        if assign_role_form.is_valid():
            users = assign_role_form.cleaned_data['users']
            new_group = assign_role_form.cleaned_data['group']


            for user in users:
                # Remove old roles
                user.groups.clear()
                # Assign new role
                user.groups.add(new_group)

            messages.success(
                request,
               f"{users.count()} user(s) assigned as {new_group.name}"
            )
            return redirect('users:assign_role')
        

    context = {
        'assign_role_form': assign_role_form
    }

    return render( request, 'assign_role.html',context)



@user_passes_test(can_assign_change_role,login_url="events:no_permission")
def change_role(request,participantID):
     if request.method == "POST":
        participant = Participant.objects.get(id = participantID)
        user = participant.user
        change_role_form = ChangeRoleForm(request.POST)
        if change_role_form.is_valid():
            new_group = change_role_form.cleaned_data.get('group')
            user.groups.clear()
            user.groups.add(new_group)
            messages.success(request,f"{user.username} added to {new_group.name} Successfully")
            return redirect("users:participant_profile", participantID)







@permission_required("auth.add_group",login_url="events:no_permission")
def create_group(request):
    create_group_form = CreateGroupForm()

    if request.method == 'POST':
        create_group_form = CreateGroupForm(request.POST)

        if create_group_form.is_valid():
            group = create_group_form.save()
            messages.success(request,f"Group {group.name} has been created successfully")
            return redirect('users:create_group')
    
    return render(request,'create_group.html', {"create_group_form":create_group_form})




""" 
    if  viewer_participant == None ; then viewer is a superuser 



      samepeople = (
        viewer_participant is not None and viewer_participant.id == participant.id
    )
"""

  