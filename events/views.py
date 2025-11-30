from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.models import Event,Catagory,Participant
from events.forms import ParticipantModelForm,CatagoryModelForm,EventModelForm
from django.contrib import messages
from django.utils import timezone



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
    
    print(didsearchOccured)

    context = {
        "events": events,
        "catagories": catagories,
        "didsearchOccured":didsearchOccured
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
        contextData = Participant.objects.prefetch_related("event_participant__catagory").all()

    elif type == "previousevents":
        contextData = events.filter(eventDate__lt=today)
    
    elif type == "upcomingevents":
        contextData = events.filter(eventDate__gt=today)
    
    else:
        #todaysevents:
        contextData = events.filter(eventDate = today)

    
    context = {
        "totalEvents":totalEvents,
        "totalParticipants":totalParticipants,
        "previousEvents":previousEvents,
        "upcomingEvents":upcomingEvents,
        "contextData":contextData,
        "type": type
    }

        
        


    return render(request,"dashboard/dashboard.html",context)





def details(request,eventID):
    event = Event.objects.get(id = eventID)

    context = {"event":event}

    return render(request,"operations/details.html",context)



def editEvent(request,eventID):
    event = Event.objects.get(id = eventID)
    event_form = EventModelForm(instance = event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST,instance = event)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event Updated Successfully")
            return redirect("editEvent", eventID)
        else:
            messages.error(request,"Something Went Wrong!!!")
    
    context = {
        "form":event_form
    }

   
    return render(request,"operations/create.html",context)


def deleteEvent(request,eventID):

    if request.method == "POST":
        event = Event.objects.get(id = eventID)
        event.delete()
        messages.success(request,"Event Deleted Successfully")
        return redirect("dashboard")
    
    else:
        messages.error(request,"Something Went Wrong")
        return redirect("dashboard")



def editParticipant(request,participantID):
  
  participant = Participant.objects.get(id = participantID)
  participant_form = ParticipantModelForm(instance = participant)


  if request.method == "POST":
      participant_form = ParticipantModelForm(request.POST, instance = participant)
      if participant_form.is_valid():
          participant = participant_form.save()
          messages.success(request,"Member Edited Successfully")
          return redirect("dashboard")
    
      else:
        messages.error(request,"Something Went Wrong")
        return redirect("dashboard")

  context = {
        "form":participant_form
    }
  
  return render(request,"operations/create.html",context)




def deleteParticipant(request, participantID):

    if request.method == "POST":
        participant = Participant.objects.get(id = participantID)
        participant.delete()
        messages.success(request,"Participant Deleted Successfully")
        return redirect("dashboard")
    
    else:
        messages.error(request,"Something Went Wrong")
        return redirect("dashboard")
  
  



def create_event(request):

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event = event_form.save()
            messages.success(request,"Event Created Successfully")
            return redirect("create_event")


    if Catagory.objects.count() == 0:
        messages.warning(request,"Pleaes Create a Catagory First")
        return redirect("create_catagory")

    if Participant.objects.count() == 0:
        messages.warning(request,"Pleaes Create Participants First")
        return redirect("create_participant")

    event_form = EventModelForm()

    context = {
        "form":event_form
    }

   
    return render(request,"operations/create.html",context)



def create_participant(request):
   
   if request.method == "POST":
       participant_form = ParticipantModelForm(request.POST)
       if participant_form.is_valid():
           member = participant_form.save()
           messages.success(request,"Memebership Created Successfully")
           return redirect("create_participant")
       
   participant_form = ParticipantModelForm()
   context = {
       "form":participant_form
   }

   
           
   
   return render(request,"operations/create.html",context)
   



def create_catagory(request):

   if request.method == "POST":
        catagory_form = CatagoryModelForm(request.POST)

        if catagory_form.is_valid():
            catagory = catagory_form.save()
            messages.success(request,"Catagory Created Successfully")
            return redirect("create_catagory")
   
   catagory_form = CatagoryModelForm()
   context = {
       "form":catagory_form
   }

   

   
   return render(request,"operations/create.html",context)






def editCatagory(request,catagoryID):
    catagory = Catagory.objects.get(id = catagoryID)
    catagory_form = CatagoryModelForm(instance = catagory)

    if request.method == "POST":
        catagory_form = CatagoryModelForm(request.POST,instance = catagory)
        if catagory_form.is_valid():
            catagory = catagory_form.save()
            messages.success(request,"Catagory Updated Successfully")
            return redirect("editCatagory", catagoryID)
        else:
            messages.error(request,"Something Went Wrong!!!")
    
    context = {
        "form":catagory_form
    }

   
    return render(request,"operations/create.html",context)





def deleteCatagory(request,catagoryID):
    if request.method == "POST":
        catagory = Catagory.objects.get(id = catagoryID)
        catagory.delete()
        messages.success(request,"Catagory Deleted Successfully")
        return redirect("home")
    
    else:
        messages.error(request,"Something Went Wrong")
        return redirect("home")