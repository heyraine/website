from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.context_processors import csrf

# Create your views here.
def home(request):
    template = loader.get_template('simple/index.html')
    return HttpResponse(template.render(request))
    #return HttpResponse('''Home Page''')

def raine(request):
    """
    hello = 'Raine'
    response = HttpResponse()
    response.write(u'<h1>Hi {0}</h1>'+email.format(hello))
    return response
    """
    if request.method == 'POST':
        c = {}
        c.update(csrf(request))
        search_id = request.POST.get('textfield', None)
        hello = 'Raine'
        response = HttpResponse()
        response.write(u'<h1>Hi {0}</h1>'.format(hello))
        response.write(search_id)
        #return render_to_response(response,c)
        return HttpResponse(response)
    else:
        return HttpResponse('''Raine''')
