import json, unittest, StringIO # Just for the sake of having a dummy stram object...
from django.http import HttpResponse

import util
from util import debug
from models import User
import models_test
# Error codes
# Well, we have some error codes to hand out before we even hit User.login
# So off they go into util...

# CsrfViewMiddleware is supposed to shut up if we set the Content-Type correctly. Guess not...
MIME_APPLICATION_JSON = "application/json"
    
class checked(object):
    # Please. We know we'll always be receiving POST.
    method = "POST"
    
    def __init__(self, required_params):
        # self.method = method.upper()
        self.required_params = required_params
    
    def __call__(self, f):
        def check_params(request, *args, **kwargs):
            # Is this even the right type?
            if not request.method == self.method:
                debug("Wrong method type, bailing")
                return response(util.ERR_BAD_CREDENTIALS)
            
            request.decoded_payload = json.loads(request.body)
            
            for field in self.required_params:
                # if field not in getattr(request, self.method):
                if field not in request.decoded_payload:
                    debug("{field} not in request_params={rp}".format(field = field, rp = request.decoded_payload))
                    return response(util.ERR_BAD_CREDENTIALS)
                    
            return f(request, *args, **kwargs)
        return check_params
    
def response(code, **addl):
    return HttpResponse(json.dumps(dict([("errCode", code)] + addl.items())), content_type = MIME_APPLICATION_JSON)

@checked(["user", "password"])
def login(request):
    rv = User.login(request.decoded_payload["user"], request.decoded_payload["password"])
    if rv > 0:
        return response(util.SUCCESS, count = rv)
    return response(rv)
    
@checked(["user", "password"])
def add(request):
    rv = User.add(request.decoded_payload["user"], request.decoded_payload["password"])
    if rv > 0:
        return response(util.SUCCESS, count = rv)
    return response(rv)
    
@checked([])
def reset_fixture(request):
    debug("Fixture reset requested, deleting all Users")
    rv = User.TESTAPI_resetFixture()
    return response(rv)
    
@checked([])
def invoke_unittests(request):
    debug("Unit test invocation requested")
    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(models_test.TestAdditional)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)
    debug(result)
    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(rv), content_type = MIME_APPLICATION_JSON)




