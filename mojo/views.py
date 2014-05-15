from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Context, RequestContext
from mojo.models import MojoUser
from hashlib import sha256
from django.shortcuts import redirect
import xlrd
from tools import instamojo

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
    try:
        request.session['login']
    except KeyError :
        return redirect('/')

    template = loader.get_template('upload.html')
    errorDict = {}
    errorDict['readError'] = False
    errorDict['offers'] = []
    if len(request.FILES.keys()) > 0 :
        data = request.FILES['excelfile'].read()
        try :
            wb = xlrd.open_workbook(file_contents = data)
            login = request.session['login']
            obj = MojoUser.objects.filter(login = login)[0]
            sheets = wb.sheet_names()
            api = instamojo.API(obj.mojoToken)

            for name in sheets:
                worksheet = wb.sheet_by_name(name)
                num_rows = worksheet.nrows
                if(worksheet.ncols < 9 ):
                    raise xlrd.XLRDError
                for i in range(num_rows):
                    offerDict = {}
                    argDict = {}
                    argDict['title'] = worksheet.cell_value(i,0)
                    argDict['description'] = worksheet.cell_value(i,1)
                    argDict['currency'] = worksheet.cell_value(i,2)
                    argDict['base_price'] = str(worksheet.cell_value(i,3))
                    argDict['quantity'] = str(int(worksheet.cell_value(i,4)))
                    argDict['start-date'] = worksheet.cell_value(i,5)
                    argDict['end-date'] = worksheet.cell_value(i,6)
                    argDict['timezone'] = worksheet.cell_value(i,7)
                    argDict['venue']  = worksheet.cell_value(i,8)
                    argDict['redirect-url'] = worksheet.cell_value(i,9)

                    for k in argDict.keys() :
                        argDict[k] = str(argDict[k])
                    #print 'quantity = ',type(argDict['quantity'])
                    reply = api.offer_create(**argDict)
                    offerDict['title'] = argDict['title']
                    offerDict['success'] = reply[u'success']
                    
                    

                    try:
                        errors = reply[u'errors']
                        offerDict['error'] = errors
                        for k in errors.keys():
                            val = errors[k]
                            del errors[k]
                            errors[str(k)] = [str(x) for x in val]
                            
                    except KeyError:
                        offerDict['error'] = ''

                    errorDict['offers'].append(offerDict)

            
        except xlrd.XLRDError :
            errorDict['readError'] = True
        
            
    c = RequestContext(request,errorDict)
    return HttpResponse(template.render(c))

def logout(request):
    del request.session['login']
    return redirect('/')
