from django.shortcuts import render,redirect
from events.models import Event,Catagory
from users.models import Participant
from events.forms import CatagoryModelForm,EventModelForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.db.models import Prefetch





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





def home(request):
    event_query = request.GET.get("eventSearch", "").strip().lower()
    catagory_query = request.GET.get("catagorySearch", "").strip().lower()

    events = Event.objects.none()
    catagories = Catagory.objects.none()
    didsearchOccured = False

    


    if event_query:
        events = Event.objects.filter(eventName__icontains=event_query).select_related("catagory").prefetch_related("participants")
        print(f"Inside event_query")
        didsearchOccured = True
    elif catagory_query:
        catagories = Catagory.objects.filter(catagoryName__icontains=catagory_query).prefetch_related("event_catagory")
        print(f"Inside catagory_query")
        didsearchOccured = True
    
    # print(didsearchOccured)

    role = get_user_role(request.user)

    context = {
        "events": events,
        "catagories": catagories,
        "didsearchOccured":didsearchOccured,
        "role":role
    }

    return render(request, "homepage.html",context)





def dashboard(request):
    type = request.GET.get("type","todaysevents")

    events = Event.objects.select_related("catagory").prefetch_related("participants").all()


    totalEvents = 0
    totalParticipants = Participant.objects.count()
    previousEvents = 0
    upcomingEvents = 0
    today = timezone.localdate()

    for event in events:
        totalEvents+=1

        if event.eventDate < today:
            previousEvents+=1
        
        if event.eventDate > today:
            upcomingEvents+=1

    
    if type == "totalevents":
        contextData = events
    
    elif type == "totalparticipants":
        # contextData = Participant.objects.prefetch_related("rsvp_events__catagory").all()
        contextData = Participant.objects.select_related('user').prefetch_related("rsvp_events").all()

    elif type == "previousevents":
        contextData = events.filter(eventDate__lt=today)
    
    elif type == "upcomingevents":
        contextData = events.filter(eventDate__gt=today)
    
    else:
        #todaysevents:
        contextData = events.filter(eventDate = today)

    
    role = get_user_role(request.user)

    
    context = {
        "totalEvents":totalEvents,
        "totalParticipants":totalParticipants,
        "previousEvents":previousEvents,
        "upcomingEvents":upcomingEvents,
        "contextData":contextData,
        "type": type,
        "role":role,
    }

        
        


    return render(request,"dashboard/dashboard.html",context)





def details(request,eventID):
    event = (   Event.objects.select_related("catagory").
                prefetch_related(Prefetch("participants",queryset=Participant.objects.select_related("user"))).get(id = eventID) 
            )
    # event = Event.objects.get(id = eventID)
    role = get_user_role(request.user)
    can_view = (role == "Admin" or role == "Organizer")
    context = {"event":event,
               "can_view":can_view,
               }
    return render(request,"operations/details.html",context)


@permission_required("events.change_event",login_url="events:no_permission")
def editEvent(request,eventID):
    event = Event.objects.get(id = eventID)
    event_form = EventModelForm(instance = event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST,request.FILES,instance = event)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event Updated Successfully")
            return redirect("events:editEvent", eventID)
        else:
            messages.error(request,"Something Went Wrong!!!")
    
    context = {
        "form":event_form
    }

   
    return render(request,"operations/create_ev_cat.html",context)



@permission_required("events.delete_event",login_url="events:no_permission")
def deleteEvent(request,eventID):

    if request.method == "POST":
        event = Event.objects.get(id = eventID)
        event.delete()
        messages.success(request,"Event Deleted Successfully")
        return redirect("events:dashboard")
    
    else:
        messages.error(request,"Something Went Wrong")
        return redirect("events:dashboard")




  

@permission_required("events.add_event",login_url="events:no_permission")
def create_event(request):

    if request.method == "POST":
        event_form = EventModelForm(request.POST,request.FILES)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event Created Successfully")
            return redirect("events:create_event")
        else:
             messages.error(request, event_form.errors)
             return redirect("events:create_event")
           


    if Catagory.objects.count() == 0:
        messages.warning(request,"Pleaes Create a Catagory First")
        return redirect("events:create_catagory")


    event_form = EventModelForm()

    context = {
        "form":event_form
    }

   
    return render(request,"operations/create_ev_cat.html",context)






   


@permission_required("events.add_catagory",login_url="events:no_permission")
def create_catagory(request):

   if request.method == "POST":
        catagory_form = CatagoryModelForm(request.POST)

        if catagory_form.is_valid():
            catagory = catagory_form.save()
            messages.success(request,"Catagory Created Successfully")
            return redirect("events:create_catagory")
   
   catagory_form = CatagoryModelForm()
   context = {
       "form":catagory_form
   }

   

   
   return render(request,"operations/create_ev_cat.html",context)





@permission_required("events.change_catagory",login_url="events:no_permission")
def editCatagory(request,catagoryID):
    catagory = Catagory.objects.get(id = catagoryID)
    catagory_form = CatagoryModelForm(instance = catagory)

    if request.method == "POST":
        catagory_form = CatagoryModelForm(request.POST,instance = catagory)
        if catagory_form.is_valid():
            catagory = catagory_form.save()
            messages.success(request,"Catagory Updated Successfully")
            return redirect("events:editCatagory", catagoryID)
        else:
            messages.error(request,"Something Went Wrong!!!")
    
    context = {
        "form":catagory_form
    }

   
    return render(request,"operations/create_ev_cat.html",context)




@permission_required("events.delete_catagory",login_url="events:no_permission")
def deleteCatagory(request,catagoryID):
    if request.method == "POST":
        catagory = Catagory.objects.get(id = catagoryID)
        catagory.delete()
        messages.success(request,"Catagory Deleted Successfully")
        return redirect("home")
    
    else:
        messages.error(request,"Something Went Wrong")
        return redirect("home")
    




def rsvp(request,eventID):
    user =request.user

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
        return render(request,"no_permission.html")
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
