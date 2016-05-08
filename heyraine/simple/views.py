from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader, Context, Template
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import subprocess, sys, os
from simple.models import room as room_DB

from .forms import EmailForm


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
    #request argument: email inputted by user
    email = request.session['email']

    #create room, add user
    auth = "NmQ5MGQ0NzYtOWI4OS00ODc1LTgyYmItZGE2YzdhMjU1OGM2NDQ0OWVhYmEtNGJl"
    headers = {"Authorization":"Bearer " + auth}
    room_json = room.makeRoom(headers)
    roomID = (room_json['id'])
    person_json = room.addPerson(roomID,email)
    personID = person_json['personId']

    template = loader.get_template('simple/raine.html')
    context = Context({"room_url": "https://web.ciscospark.com/#/rooms/","roomID":roomID})

    rmdb = room_DB(roomID=roomID, personID=personID)
    rmdb.save()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    #subprocess.Popen(['Python', os.path.join(BASE_DIR, 'simple/room_miniscript.py')])

    p = subprocess.Popen(['Python', os.path.join(BASE_DIR, 'simple/room_miniscript.py'+' -r '+roomID+' -p '+personID)],stdin=subprocess.PIPE,shell=True)
    p.communicate(roomID+'\n'+personID)[0]

    #delete room
    #room.deleteRoom(roomID, room_json)

    return HttpResponse(template.render(context))
