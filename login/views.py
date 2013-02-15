import json, unittest
from django.http import HttpResponse
from django.template import Context, loader
from login.models import User
import models_test

# import testAdditional
SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

def controll(obj, **args):
    return HttpResponse(json.dumps(dict([("errCode", code)] + addl.items())), content_type = MIME_APPLICATION_JSON)


def login(request):
    # Check that the request method is correct.
    if request.method != "POST":
            return controll(ERR_BAD_CREDENTIALS) 
    # Check all parameters are present
    parameters = json.loads(request.body)
    for p in ["user", "password"]:
            if p not in parameters:
                return controll(ERR_BAD_CREDENTIALS)
    user = User.login(parameters["user"], parameters["password"])
    if user > 0:
        return controll(SUCCESS, count = user)
    else:
        return controll(user)
    
def add(request):
    if request.method != "POST":
            return controll(ERR_BAD_CREDENTIALS) 
    parameters = json.loads(request.body)
    for p in ["user", "password"]:
            if p not in parameters:
                return controll(ERR_BAD_CREDENTIALS)
    user = User.add(parameters["user"], parameters["password"])
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
        suite = unittest.TestLoader().loadTestsFromTestCase(models_test.TestAdditional)
        result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)
        user = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
        return HttpResponse(json.dumps(user), content_type = "application/json")
