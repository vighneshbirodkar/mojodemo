from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context
from mojo.models import MojoUser

# Create your views here.
MAX_ATTEMPTS = 100
def index(request):
    
    template = loader.get_template('index.html')
    errorDict = {}
    
    errorDict['mismatch'] = False
    errorDict['noLogin'] = False
    errorDict['noPass'] = False
    errorDict['noMore'] = False

    if  len(request.REQUEST.keys()) > 0 :
        
        try:
            request.session['count'] += 1
        except KeyError:
            request.session['count'] = 1

        if request.session['count'] > MAX_ATTEMPTS :
            errorDict['noMore'] = True
        if len( request.REQUEST['login'] ) == 0 :
            errorDict['noLogin'] = True
        if len( request.REQUEST['password'] ) == 0 :
            errorDict['noPass'] = True
    
#        if not errorDict['noMore'] : 
#            print '***********'
#            print MojoUser.objects.filter(login=request.REQUEST['login'])
    c = Context(errorDict)

    return HttpResponse(template.render(c))


