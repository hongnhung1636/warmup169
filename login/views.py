# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from warmupApp.models import User
# import the logging library
from django.views.decorators.csrf import csrf_protect
import logging
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import sys 
from os import curdir, sep
import os
from django.http import Http404
import json
import models
import cgi
import tempfile
import traceback
g_user = models.User()


SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

# Get an instance of a logger
log = logging.getLogger(__name__)
@csrf_exempt
def index(request): 
    if request.method == "POST":
        if request.path.find("/users/")==0:
            return UserController(request)
        elif request.path.find("/TESTAPI/")==0:
            return TESTController(request)
        else:
            raise Http404
    elif request.method=="GET":
        if request.path not in ["/client.html","/client.css","/client.js"]:
            raise Http404
        else:
            mimeType="text/html"
            if request.path.endswith(".css"):
                mimeType = "text/css"
            elif request.path.endswith(".js"):
                mimeType = "text/javascript"
            return render_to_response('warmupApp'+request.path,mimetype=mimeType)

@csrf_exempt
def TESTController(request):
    if request.path=="/TESTAPI/resetFixture":
        g_user.TESTAPI_resetFixture()
        return HttpResponse(json.dumps({'errCode': SUCCESS}),content_type="application/json" )
    elif request.path== "/TESTAPI/unitTests":
        (ofile, ofileName) = tempfile.mkstemp(prefix="userCounter")
            try:
                errMsg = ""     # We accumulate here error messages
                output = ""     # Some default values
                totalTests = 0
                nrFailed   = 0
                while True:  # Give us a way to break
                    # Find the path to the server installation
                    thisDir = os.path.dirname(os.path.abspath(__file__))
                    cmd = "make -C "+thisDir+" unit_tests >"+ofileName+" 2>&1"
                    print "Executing "+cmd
                    code = os.system(cmd)
                    if code != 0:
                        # There was some error running the tests.
                        # This happens even if we just have some failing tests
                        errMsg = "Error running command (code="+str(code)+"): "+cmd+"\n"
                        # Continue to get the output, and to parse it
                        
                    # Now get the output
                    try:
                        ofileFile = open(ofileName, "r")
                        output = ofileFile.read()
                        ofileFile.close ()
                    except:
                        errMsg += "Error reading the output "+traceback.format_exc()
                        # No point in continuing
                        break
                    
                    print "Got "+output
                    # Python unittest prints a line like the following line at the end
                    # Ran 4 tests in 0.001s
                    m = re.search(r'Ran (\d+) tests', output)
                    if not m:
                        errMsg += "Cannot extract the number of tests\n"
                        break
                    totalTests = int(m.group(1))
                    # If there are failures, we will see a line like the following
                    # FAILED (failures=1)
                    m = re.search('rFAILED.*\(failures=(\d+)\)', output)
                    if m:
                        nrFailures = int(m.group(1))
                    break # Exit while

                # End while
                resp = { 'output' : errMsg + output,
                         'totalTests' : totalTests,
                         'nrFailed' : nrFailed }
        return HttpResponse(json.dumps(resp),content_type="application/json" )
            finally:
                os.unlink(ofileName)
                
            
        else:
            raise Http404

@csrf_exempt
def UserController(request):
    inData = json.loads(request.body)
    #sys.stderr.write(str(inData))
    #inData = dict(request.POST)
    #sys.stderr.write(str(inData.keys()))
    #sys.stderr.write(str(type(inData)))
    inUserName = inData["user"]
    inpassword = inData["password"]
    if request.path == "/users/login":    
            rval = g_user.login(inUserName, inpassword)
    elif request.path=="/users/add":
            rval = g_user.add(inUserName, inpassword)
    else:
        raise Http404
    if rval<0:
        return HttpResponse(json.dumps({'errCode': rval}),content_type="application/json" )
    else:
        return HttpResponse(json.dumps({'errCode': SUCCESS, 'count': rval}),content_type="application/json" )


