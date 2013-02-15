import json, unittest
from django.http import HttpResponse
from django.template import Context, loader
from login.models import User

import testAdditional
SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

    
class index(object):
    post = "POST"
    def __init__(self, require):
        self.require = require
    
    def __call__(self, call):
        def check(request, *args, **args1):
            if request.post != self.post:
                return controll(ERR_BAD_CREDENTIALS)
            request.decoded_payload = json.loads(request.body)
            for obj in self.require:
                if obj not in request.decoded_payload:
                    return controll(ERR_BAD_CREDENTIALS)
            return call(request, *args, **args1)
        return check
    
def login(request):
    user = User.login(request.decoded_payload["user"], request.decoded_payload["password"])
    if request.path=="/users/add":
        if user > 0:
            return controll(SUCCESS, count = user)
        else:
            return controll(user)
    
def add(request):
    user = User.add(request.decoded_payload["user"], request.decoded_payload["password"])
    if request.path == "/users/add":    
        if user > 0:
            return controll(SUCCESS, count = user)
        else:
            return controll(user)
    
def resetFixture(request):
    if request.path=="/TESTAPI/resetFixture":
        user = User.TESTAPI_resetFixture()  
        return controll(user)
    
def unittestControll(request):
    if request.path== "/TESTAPI/unitTests":
        suite = unittest.TestLoader().loadTestsFromTestCase(testAdditional.TestAdditional)
        result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)
        user = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
        return HttpResponse(json.dumps(user), content_type = "application/json")

def controll(obj, **args):
    return HttpResponse(json.dumps(dict([("errCode", obj)] + args.items())), content_type = "application/json")

