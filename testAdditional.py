#!/usr/bin/env python

# We ought to be using Django TestCases and have this in the tests.py,
# but we have no test database to run on and no permissions to do so.
# Poor man's tests we shall remain.

# By the way, this doesn't strictly follow the format of testSimple.py.
# It is quite unfortunate, but this is already simple in the unittest format...

# There are 13 tests in this file.
# Three of them are not run in unit test mode.

# This test runner has a facility to load the Django exceptions in lynx
# for interactive debugging. 

# Endpoint setting priority: TEST_SERVER, argument input, default ENDPOINT

import requests, json, subprocess, unittest, sys, random, argparse, os, urlparse, random

ENDPOINT = "http://localhost:5000"
INTERACTIVE = True

# Error codes, copied from logincounter.util
SUCCESS             = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS     = -2
ERR_BAD_USERNAME    = -3
ERR_BAD_PASSWORD    = -4

p = argparse.ArgumentParser(description = "Unit tests for logincounter backend")
p.add_argument("--interactive", "-i", action = "store_true", help = "Invoke Lynx when a Django Exception is encountered")
p.add_argument("--unit", "-u", action = "store_true", help = "Run unit tests instead of functional tests")
p.add_argument("endpoint", default = ENDPOINT, nargs = "?", help = "The endpoint to run the tests at")

# Pass on extra args to unittest.
args, extra = p.parse_known_args()

INTERACTIVE = args.interactive

# unittest `discover` gets passed on to us unknowningly. Dispose of this argument
# if it doesn't come with a schema.
url = urlparse.urlparse(args.endpoint)
if url.scheme != "":
    ENDPOINT = args.endpoint

if "TEST_SERVER" in os.environ and os.environ["TEST_SERVER"] != "":
    ENDPOINT = os.environ["TEST_SERVER"]
    
if args.unit or "DJANGO_SETTINGS_MODULE" in os.environ: # Unit testing if we're running in Django
    args.unit = True # If we snuffed it out with DJANGO_SETTINGS_MODULE
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warmup.settings")
    from login.models import User
    
    # We're just pretending! It's not really Django about these parts!
    terrible_urlconf = {
        "/users/login": User.login,
        "/users/add": User.add,
        "/TESTAPI/resetFixture": User.TESTAPI_resetFixture,
        "/TESTAPI/unitTests": lambda: None # We can't invoke the unit tests, we are the unit tests
    }
    
sys.argv = sys.argv[0:1] + extra

def request(type, url, **params):
    # Don't ever do this. Ever. If you do, shoot yourself out of CS169.
    if args.unit:
        target = terrible_urlconf[url]
        print target
        return target(**params)
        
    else:
        param_type = "params" if type is "get" else "data"
        params = json.dumps(params)
        url = ENDPOINT + url
        r = getattr(requests, type)(**{"url": url, param_type: params})
        if "Exception Value" in r.text and INTERACTIVE:
            p = subprocess.Popen("lynx -stdin", shell = True, stdin = subprocess.PIPE)
            p.communicate(input = r.text)
            _ = lambda: None
            _.text = "<Django Exception>"
            return _
        else:
            return r
        
def random_string(n = 10):
    return "".join(map(lambda _: chr(int(random.random() * 57) + 65), range(0, n)))

class LoginCounterTest(unittest.TestCase):
    test_user = random_string()
    test_password = random_string()
    
    def assertErrCode(self, errCode, response):
        if args.unit:
            self.assertEqual(errCode, response)
        else:
            self.assertEqual(errCode, json.loads(response.text)["errCode"])
        
    def test_00_reset(self):
        r = request("post", "/TESTAPI/resetFixture")
        self.assertErrCode(SUCCESS, r)
        
    @unittest.skipIf(args.unit, "Test not applicable")
    def test_01_wrong_method(self):
        # This resource doesn't take a GET. In fact, none of them do.
        # This test doesn't make sense for unit testing.
        r = request("get", "/users/login")
        self.assertErrCode(ERR_BAD_CREDENTIALS, r)
        
    @unittest.skipIf(args.unit, "Test not applicable")
    def test_02_not_enough_parameters(self):
        r = request("post", "/users/login")
        self.assertErrCode(ERR_BAD_CREDENTIALS, r)
        
    def test_03_user_doesnt_exist(self):
        r = request("post", "/users/login", user = random_string(), password = random_string())
        self.assertErrCode(ERR_BAD_CREDENTIALS, r)
        
    def test_04_empty_username_add(self):
        # Empty username to add.
        r = request("post", "/users/add", user = "", password = "poop")
        self.assertErrCode(ERR_BAD_USERNAME, r)
        
    def test_05_long_username_add(self):
        # Too long username
        r = request("post", "/users/add", user = random_string(150), password = random_string())
        self.assertErrCode(ERR_BAD_USERNAME, r)
        
    def test_06_long_password_add(self):
        # Too long password
        r = request("post", "/users/add", user = random_string(), password = random_string(150))
        self.assertErrCode(ERR_BAD_PASSWORD, r)
        
    def test_07_1_add(self):
        r = request("post", "/users/add", user = self.test_user, password = self.test_password)
        self.assertErrCode(SUCCESS, r)
        
    def test_07_2_add_existing(self):
        r = request("post", "/users/add", user = self.test_user, password = self.test_password)
        self.assertErrCode(ERR_USER_EXISTS, r)
        
    def test_07_3_add_another(self):
        r = request("post", "/users/add", user = random_string(), password = random_string())
        self.assertErrCode(SUCCESS, r)
        r = request("post", "/users/add", user = random_string(), password = random_string())
        self.assertErrCode(SUCCESS, r)
        
    def test_08_bad_login(self):
        r = request("post", "/users/login", user = self.test_user, password = random_string())
        self.assertErrCode(ERR_BAD_CREDENTIALS, r)
    
    def test_09_login(self):
        r = request("post", "/users/login", user = self.test_user, password = self.test_password)
        r = 1 if args.unit and r >= 1 else r
        self.assertErrCode(SUCCESS, r)
        
    # Another test to assert the number of logins
    def test_10_lots_of_logins(self):
        times = random.randrange(20)
        for i in range(times):
            r = request("post", "/users/login", user = self.test_user, password = self.test_password)
            count = json.loads(r.text)["count"] if not args.unit else r
        self.assertEqual(count, times + 2)
        
    @unittest.skipIf(args.unit, "Test not applicable")
    def test_99_invoke_unittests(self):
        # For some reason the python json deserializer doesn't change \n back into newlines. Whatever...
        r = request("post", "/TESTAPI/unitTests")
        result = json.loads(r.text, object_hook = lambda o: o.replace("\\n", "\n") if type(o) == str else o)
        self.assertEqual(result["nrFailed"], 0)

if __name__ == '__main__':
    unittest.main()
