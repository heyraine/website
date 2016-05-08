from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from .forms import EmailForm
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
    email = request.session['email']
    print(email)
    response = HttpResponse()
    response.write(email)
    return HttpResponse(response)
