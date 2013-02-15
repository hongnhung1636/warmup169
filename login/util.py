import inspect, traceback, os
from django.conf import settings

# Error codes
SUCCESS             = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS     = -2
ERR_BAD_USERNAME    = -3
ERR_BAD_PASSWORD    = -4

MAX_TEXT_LEN = 128

def debug(spam, frames_up = 2):
    if settings.DEBUG:
        stack_trace = traceback.extract_stack(inspect.currentframe())
        info = list(stack_trace[-frames_up])
        info[0] = os.path.basename(info[0])
        print "[spam] {file}:{line}@{method}: {spam}".format(spam = spam, file = info[0], line = info[1], method = info[2])

def log_exception(e):
    debug("{module}.{cls}: {message}".format(module = e.__class__.__module__, cls = e.__class__.__name__, message = e.message), 3)