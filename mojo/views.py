from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from mojo.models import MojoUser
from hashlib import sha256
from django.shortcuts import redirect

# Create your views here.
MAX_ATTEMPTS = 100
def index(request):
    
    try:
        request.session['login']
        return redirect('/upload')
    except KeyError :
        pass

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
    

        if not errorDict['noMore'] : 
            #print '***********',request.REQUEST['login']
            objList =  MojoUser.objects.filter(login=request.REQUEST['login'])
            if len(objList) == 0 :
                errorDict['mismatch'] = True
            else:
                obj = objList[0]
                #print "****", sha256(request.REQUEST['password']).hexdigest , obj.passwdHash
                if sha256(request.REQUEST['password']).hexdigest() == obj.passwdHash :
                    request.session['login'] = obj.login
                    return redirect("/upload")
                else:
                    errorDict['mismatch'] = True
    c = RequestContext(request, errorDict)

    return HttpResponse(template.render(c))


def upload(request):
    template = loader.get_template('upload.html')
    c = RequestContext(request,{})
    if len(request.FILES.keys()) > 0 :
        pass
    return HttpResponse(template.render(c))

def logout(request):
    del request.session['login']
    return redirect('/')
