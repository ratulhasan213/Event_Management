from django.shortcuts import render,redirect
from users.forms import UserForm,ParticipantModelForm,LoginForm,UserEditForm,AssignRoleForm,CreateGroupForm,ChangeRoleForm,ChangePasswordForm,PasswordResetMyForm,PasswordResetConfirmForm
from users.models import Participant
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.views.generic import UpdateView,CreateView,DetailView,DeleteView,FormView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy

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



class SingUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = "sign_up.html"
    success_url = reverse_lazy("users:sign_up")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = context.pop("form")
        return context
    

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        messages.success(self.request,"Memebership Created Successfully.Please check your email")
        return redirect(self.success_url)
    





class ActivateUser(View):

    def get(self,request,user_id,token):
        status = "invalid"

        try:
            user = User.objects.get(id = user_id)
            if default_token_generator.check_token(user,token):
                
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    status = "activated"
                else:
                    status = "alreadyActivated"
                
            
           
            return render(request,"user_activation.html",{"status":status})
        
        except User.DoesNotExist:
         
           return HttpResponse("user does not exist")



class Login(LoginView):
    form_class = LoginForm
    template_name = "log_in.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("users:my_profile")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = context.pop("form")
        return context
    



class LogOut(LogoutView):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
             messages.success(request,f"{request.user.username} logged out successfully")
        else:
            messages.warning(request,"please Login first")

        return super().dispatch(request, *args, **kwargs)
    

        



#authentication enough
class MyProfile(LoginRequiredMixin,View):

    login_url = "users:log_in"

    def handle_no_permission(self):
        messages.warning(self.request,"please Login first")
        return redirect(self.login_url)
    
    def get(self,request,*args,**kwargs):
        participant = getattr(request.user,'participant',None)
        return redirect(
        "users:participant_profile",
        participant.id
       )
        

    




class ParticipantProfile(LoginRequiredMixin,DetailView):

    model = Participant
    template_name = "participant_profile.html"
    context_object_name = "participant" # object = participant (look at model)
    login_url = "users:log_in"
    pk_url_kwarg = "participantID"



    def handle_no_permission(self):
        messages.warning(self.request,"please Login first")
        return redirect(self.login_url)

    def get_queryset(self):
        return Participant.objects.select_related("user").prefetch_related("rsvp_events")
    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        viewer = self.request.user
        events = self.object.rsvp_events.all()  # self.object = participant
        participant_role = get_user_role(self.object.user)
        viewer_role = get_user_role(self.request.user)

        can_view_form = (viewer.is_superuser or 
                        (participant_role!="Admin" and viewer.groups.filter(name = "Admin").exists())
                        )
        
        context["viewer_role"] = viewer_role
        context["participant_role"] = participant_role
        context["events"] = events
        context["change_role_form"] = ChangeRoleForm()
        context["can_view_form"] = can_view_form
        context["is_self_viewing"] = viewer == self.object.user
        context["membersince"] = self.object.user.date_joined
        context["lastlogin"] = self.object.user.last_login

        return context
    


class EditParticipant(UserPassesTestMixin,UpdateView):
    model = Participant
    form_class = ParticipantModelForm
    template_name = "sign_up.html"
    login_url = "events:no_permission"
    pk_url_kwarg = "participantID"



    def test_func(self):
        user = self.get_object().user
        viewer = self.request.user
        role = get_user_role(viewer)

        return role == "Admin" or  viewer.is_superuser or user == viewer


    def handle_no_permission(self):
        # optional: can raise 403 or redirect
        return redirect(self.login_url)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participant_form"] = context.pop("form")
        user = getattr(self.object,"user",None)
        if self.request.POST:
            context["user_form"] = UserEditForm(self.request.POST,self.request.FILES,instance = user)
        else:
            context["user_form"] = UserEditForm(instance = user)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context["user_form"]

        if user_form.is_valid():
            user_form.save()
            self.object = form.save()
            messages.success(self.request, "Profile updated successfully") 
            return redirect("users:participant_profile", self.object.id)
        
        return self.form_invalid(form)
    

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong")
        return self.render_to_response(self.get_context_data(form = form))
    
        
        


class DeleteParticipant(UserPassesTestMixin,DeleteView):
    model = Participant
    pk_url_kwarg = "participantID"
    success_url = reverse_lazy("events:dashboard")
    login_url = "events:no_permission"

    def test_func(self):
        user = self.get_object().user
        viewer = self.request.user
        role = get_user_role(viewer)
        return viewer.is_superuser or role == "Admin"
    
    def form_valid(self,form):
        user = self.get_object().user
        viewer = self.request.user

        if user == viewer:
            messages.error(self.request, "You cannot delete yourself!")
            return redirect(self.success_url)
        
        if user.is_superuser:
            messages.error(self.request, "Super-User cannot be deleted!")
            return redirect(self.success_url)
        
        if not viewer.is_superuser and get_user_role(user) == "Admin":
            messages.error(self.request, "Only super user can delete admin!")
            return redirect(self.success_url)
        
        name = user.username
        user.delete()
        messages.success(self.request, f"{name} deleted successfully")
              
        return redirect(self.success_url)
    
    def get(self, request, *args, **kwargs):
        messages.error(request,"Invalid get request")
        return redirect(self.success_url)






class AssignRole(UserPassesTestMixin,FormView):
    form_class = AssignRoleForm
    template_name = "assign_role.html"
    login_url = "events:no_permission"


    def test_func(self):
        return can_assign_change_role(self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assign_role_form"] = context.pop("form")
        return context
    


    def form_valid(self, form):
        users = form.cleaned_data['users']
        new_group = form.cleaned_data['group']
        
        for user in users:
            user.groups.clear()
            user.groups.add(new_group)
    
        messages.success(
                self.request,
                f"{users.count()} user(s) assigned as {new_group.name}"
            )
        return redirect('users:assign_role')
    



class ChangeRole(UserPassesTestMixin,UpdateView):
    model = Participant
    form_class = ChangeRoleForm
    pk_url_kwarg = "participantID"
    login_url="events:no_permission"

    def test_func(self):
        return can_assign_change_role(self.request.user)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_role_form"] = context.pop("form")
        return context
    
    
    

    def form_valid(self, form):
        
            new_group = form.cleaned_data.get('group')

            user = self.get_object().user
            user.groups.clear()
            user.groups.add(new_group)

            messages.success(self.request,f"{user.username} added to {new_group.name} Successfully")
            return redirect("users:participant_profile", self.get_object().pk)




class CreateGroup(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Group
    form_class = CreateGroupForm
    login_url="events:no_permission"
    permission_required = "auth.add_group"
    template_name = "create_group.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_group_form"] = context.pop("form")
        return context
    
    def form_valid(self, form):
        group = form.save()
        messages.success(self.request,f"Group {group.name} has been created successfully")
        return redirect('users:create_group')






class ChangePassword(PasswordChangeView):
    template_name = "change_password.html"
    form_class = ChangePasswordForm
    success_url = reverse_lazy('users:password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["password_change_form"] = context.pop("form")
        return context
    


class ChangePasswordDone(PasswordChangeDoneView):
    template_name = "change_password_done.html"




class ResetPassword(PasswordResetView):
    template_name = "reset_password.html"
    form_class = PasswordResetMyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = self.request.get_host()
        return context
    


    def form_valid(self, form):
        messages.success(self.request, "A reset email sent please check your email")
        return super().form_valid(form)
    




class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = "reset_password.html"
    success_url = reverse_lazy('users:log_in')


    def form_valid(self, form):
        messages.success(self.request, "Password reset successfully")
        return super().form_valid(form)

        
    
    




""" 
    





"""

  