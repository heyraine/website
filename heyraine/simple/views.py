from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader, Context, Template
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import subprocess, sys, os
from simple.models import room as room_DB

from .forms import EmailForm, StartForm


import room
#email = ""

# Create your views here.
def home(request):
    #template = loader.get_template('simple/index.html')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmailForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            email = form.cleaned_data['email']
            # redirect to a new URL:
            #url = reverse('raine', kwargs={'email': email})
            request.session['email'] = email
            return HttpResponseRedirect('/raine/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmailForm()

    return render(request, 'simple/index.html', {'form': form})

def raine(request):
    """
    hello = 'Raine'
    response = HttpResponse()
    response.write(u'<h1>Hi {0}</h1>'+email.format(hello))
    return response
    """

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StartForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            start = form.cleaned_data['start']
            # redirect to a new URL:
            #url = reverse('raine', kwargs={'email': email})
            request.session['start'] = start

            room_ID = room_DB.objects.get('roomID')
            person_ID = room_DB.objects.get('personID')

            count = 0
            room.sendFirstMessage(room_ID)
            #while (count < 10): #run 3 times. 3 responses from user,
                                #3 responses from Watson.
            messages_json = room._getMessages(room_ID, person_ID)
            personMessage = (messages_json['items'][0]['text'])
            room.sendMessage(room_ID, personMessage)
            count += 1

            return HttpResponseRedirect('')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StartForm()
        #request argument: email inputted by user
        email = request.session['email']

        #create room, add user
        auth = "NmQ5MGQ0NzYtOWI4OS00ODc1LTgyYmItZGE2YzdhMjU1OGM2NDQ0OWVhYmEtNGJl"
        headers = {"Authorization":"Bearer " + auth}
        room_json = room.makeRoom(headers)
        room_id = (room_json['id'])
        person_json = room.addPerson(room_id,email)
        person_id = person_json['personId']

        template = loader.get_template('simple/raine.html')
        context = Context({"room_url": "https://web.ciscospark.com/#/rooms/","roomID":room_id})

        rmdb = room_DB(roomID=room_id, personID=person_id)
        rmdb.save()

        #p = subprocess.Popen(['Python', os.path.join(BASE_DIR, 'simple/room_miniscript.py'+' -r '+roomID+' -p '+personID)],stdin=subprocess.PIPE,shell=True)
        #p.communicate(roomID+'\n'+personID)[0]

        #delete room
        #room.deleteRoom(roomID, room_json)

        return HttpResponse(template.render(context))
