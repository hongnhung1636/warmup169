from django.db import models

import util
from util import debug, log_exception

# Create your models here.

class User(models.Model):
    user = models.CharField(max_length = util.MAX_TEXT_LEN)
    password = models.CharField(max_length = util.MAX_TEXT_LEN)
    count = models.IntegerField()
    
    @classmethod
    def login(cls, user, password):
        # Thank you based Django.
        try:
            user_obj = User.objects.get(user = user)
        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            log_exception(e)
            return util.ERR_BAD_CREDENTIALS
        
        if user_obj.password != password:
            debug("User '{user}' entered an incorrect password".format(user = user_obj.user))
            return util.ERR_BAD_CREDENTIALS
            
        user_obj.count += 1    
        user_obj.save()
        debug("User '{user}' successfully logged in, count is now {count}".format(user = user_obj.user, count = user_obj.count))
        
        return user_obj.count
        
    @classmethod
    def add(cls, user, password):
        # NG if user already exists.
        try:
            user_obj = User.objects.get(user = user)
        # But this is what we want.
        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            pass
        else:
            # Now bail.
            debug("User already exists.")
            return util.ERR_USER_EXISTS

        # Username can't be empty. 
        if user == "" or len(user) > util.MAX_TEXT_LEN:
            debug("Username ('{user}') is too long or too short".format(user = user))
            return util.ERR_BAD_USERNAME
        
        if len(password) > util.MAX_TEXT_LEN:
            debug("Password ('{password}') is too long".format(password = password))
            return util.ERR_BAD_PASSWORD
        
        new_user = User(user = user, password = password, count = 1)
        debug("Added user '{user}' with password '{password}'".format(user = user, password = password))
        new_user.save()
        return util.SUCCESS
        
    @classmethod
    def TESTAPI_resetFixture(self):
        User.objects.all().delete()
        return util.SUCCESS