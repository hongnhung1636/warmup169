import json, unittest, StringIO
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
    return HttpResponse(json.dumps(dict([("errCode", obj)] + args.items())), content_type = "application/json")


def login(request):
    # Check that the request method is correct.
    if request.method != "POST":
        return controll(ERR_BAD_CREDENTIALS) 
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
        user = User.TESTAPI_resetFixture()  
        return controll(user)
    
def unittestControll(request):
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(models_test.TestAdditional)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)
    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(rv), content_type = "application/json")

    
