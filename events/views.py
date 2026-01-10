from django.shortcuts import render,redirect
from events.models import Event,Catagory
from users.models import Participant
from events.forms import CatagoryModelForm,EventModelForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
# from django.contrib.auth.decorators import permission_required
from django.db.models import Prefetch
from django.views import View
from django.views.generic import TemplateView,DetailView,UpdateView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login






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





class Home(TemplateView):

    template_name = "homepage.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            event_query = self.request.GET.get("eventSearch", "").strip().lower()
            catagory_query = self.request.GET.get("catagorySearch", "").strip().lower()
            events = Event.objects.none()
            catagories = Catagory.objects.none()
            didsearchOccured = False
            if event_query:
                events = Event.objects.filter(eventName__icontains=event_query).select_related("catagory").prefetch_related("participants")
                didsearchOccured = True
            elif catagory_query:
                catagories = Catagory.objects.filter(catagoryName__icontains=catagory_query).prefetch_related("event_catagory")
                didsearchOccured = True

            role = get_user_role(self.request.user)
            context.update ( {
                "events": events,
                "catagories": catagories,
                "didsearchOccured":didsearchOccured,
                "role":role
            } )
            return context
    
    





class DashBoard(TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        type = self.request.GET.get("type","todaysevents")
        events = Event.objects.select_related("catagory").prefetch_related("participants").all()

        today = timezone.localdate()
        total_events_count = events.count()
       
        total_participants_count = Participant.objects.count()
        previousEvents = events.filter(eventDate__lt = today)
        upcomingEvents = events.filter(eventDate__gt = today)

        previous_events_count = previousEvents.count()
        upcoming_events_count = upcomingEvents.count()

      


        if type == "totalevents":
            contextData = events
    
        elif type == "totalparticipants":
            # contextData = Participant.objects.prefetch_related("rsvp_events__catagory").all()
            contextData = Participant.objects.select_related('user').prefetch_related("rsvp_events").all()

        elif type == "previousevents":
            contextData = previousEvents
    
        elif type == "upcomingevents":
            contextData = upcomingEvents
    
        else:
           #todaysevents:
           contextData = events.filter(eventDate = today)

        role = get_user_role(self.request.user)

        context.update(
            {
            "total_events_count":total_events_count,
            "total_participants_count":total_participants_count,
            "previous_events_count":previous_events_count,
            "upcoming_events_count":upcoming_events_count,
            "contextData":contextData,
            "type": type,
            "role":role,
          }) 

        return context
    



class Details(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "operations/details.html"
    pk_url_kwarg = "eventID"

    def get_queryset(self):
        qs = (Event.objects.select_related("catagory").prefetch_related(
              Prefetch("participants",queryset=Participant.objects.select_related("user")))
              )
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        role = get_user_role(self.request.user)
        can_view = (role == "Admin" or role == "Organizer")
        context["can_view"] = can_view
        return context
    
    
    




class CreateEvent(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Event
    form_class = EventModelForm
    template_name = "operations/create_ev_cat.html"
    login_url = "users:log_in"
    redirect_field_name = "next"
    permission_required = "events.add_event"
    raise_exception = False



    def dispatch(self, request, *args, **kwargs):
        if Catagory.objects.count() == 0:
            messages.warning(request,"Please Create a Category First")
            return redirect("events:create_catagory")

        return super().dispatch(request, *args, **kwargs)
    


    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.warning(self.request,"Please login first")
            return redirect_to_login(self.request.get_full_path(),self.login_url,self.redirect_field_name)
        
        return redirect("events:no_permission")


    def get_success_url(self):
        return reverse_lazy("events:create_event")
    

    def form_valid(self, form):
        messages.success(self.request,"Event Created Successfully")
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request,"Something Went Wrong!!!")
        return super().form_invalid(form)




class EditEvent(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = "operations/create_ev_cat.html"
    pk_url_kwarg = "eventID"
    login_url = "users:log_in"
    redirect_field_name = "next"
    permission_required = "events.change_event"
    raise_exception = False




    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.warning(self.request,"Please login first")
            return redirect_to_login(self.request.get_full_path(),self.login_url,self.redirect_field_name)
        
        return redirect("events:no_permission")

    
    def get_success_url(self):
        return reverse_lazy("events:editEvent",kwargs = {"eventID":self.object.id})
    
    def form_valid(self, form):
        messages.success(self.request,"Event Updated Successfully")
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request,"Something Went Wrong!!!")
        return super().form_invalid(form)
        
    


class DeleteEvent(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Event
    pk_url_kwarg = "eventID"
    login_url = "users:log_in"
    redirect_field_name = "next"
    permission_required = "events.delete_event"
    raise_exception = False

    success_url = reverse_lazy("events:dashboard")


    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.warning(self.request,"Please login first")
            return redirect_to_login(self.request.get_full_path(),self.login_url,self.redirect_field_name)
        
        return redirect("events:no_permission")
    

    def get_success_message(self, cleaned_data):
        return f"{self.object} was deleted successfully."
    
    

    
    def get(self, request, *args, **kwargs):
        messages.error(request,"Invalid get request")
        return redirect(self.success_url)
    


    


class CreateCatagory(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Catagory
    form_class = CatagoryModelForm
    template_name = "operations/create_ev_cat.html"
    login_url = "users:log_in"
    redirect_field_name = "next"
    permission_required = "events.add_catagory"
    raise_exception = False


    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.warning(self.request,"Please login first")
            return redirect_to_login(self.request.get_full_path(),self.login_url,self.redirect_field_name) 
        
        return  redirect("events:no_permission")
    

    def get_success_url(self):
        return reverse_lazy("events:create_catagory")
    

    def form_valid(self, form):
        messages.success(self.request,"Catagory Created Successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"Something went wrong")
        return super().form_invalid(form)
        
    
    


class EditCatagory(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Catagory
    form_class = CatagoryModelForm
    template_name = "operations/create_ev_cat.html"
    login_url = "users:log_in"
    redirect_field_name = "next"
    pk_url_kwarg = "catagoryID"
    permission_required = "events.change_catagory"
    raise_exception = False

    

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.warning(self.request,"Please login first")
            return redirect_to_login(self.request.get_full_path(),self.login_url,self.redirect_field_name)
        
        return redirect("events:no_permission")


    def get_success_url(self):
        return reverse_lazy("events:editCatagory",kwargs = {"catagoryID":self.object.id})


    def form_valid(self, form):
        messages.success(self.request,"Catagory Updated Successfully")
        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request,"Something Went Wrong!!!")
        return super().form_invalid(form)
    
    


class DeleteCatagory(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Catagory
    pk_url_kwarg = "catagoryID"
    login_url = "users:log_in"
    success_url = reverse_lazy("home")
    permission_required = "events.delete_catagory"
    raise_exception = False
    redirect_field_name = "next"


    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.warning(self.request,"Please login first")
            return redirect_to_login(self.request.get_full_path(),self.login_url,self.redirect_field_name)
        
        return redirect("events:no_permission")
    

    def get_success_message(self, cleaned_data):
        return f"Catagory {self.object} was deleted successfully."
    
    

    
    def get(self, request, *args, **kwargs):
        messages.error(request,"Invalid get request")
        return redirect(self.success_url)


    



class RSVP(View):

    def get(self,request,eventID,*args,**kwargs):
        user = request.user

        if not user.is_authenticated:
            messages.warning(request,"please Login first")
            return redirect("users:log_in")

        if not user.is_superuser:
            participant = getattr(user,'participant',None)
            event = Event.objects.get(id = eventID)

            if event.participants.filter(id = participant.id).exists():
                messages.error(request,f"{user.username} has already rsvp this event")
            
            else:
                event.participants.add(participant)
                messages.success(request,f"{event.eventName} added to -> {user.username} -> this account successfully")
    
        else:
            messages.error(request,"Super user cannot rsvp events")
            
        
        return redirect("events:dashboard")
        




def no_permission(request):
    if request.user.is_authenticated:
        return render(request,"operations/no_permission.html")
    else:
        messages.warning(request,"please Login first")
        return redirect("users:log_in")



    


""" 

 messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "operations/create_ev_cat.html",
                {"form": event_form}
            )

 """
