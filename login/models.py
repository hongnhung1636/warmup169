from django.db import models

# Create your models here.

MAX_TEXT_LEN = 128
SUCCESS             = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS     = -2
ERR_BAD_USERNAME    = -3
ERR_BAD_PASSWORD    = -4

class User(models.Model):
    user = models.CharField(max_length = MAX_TEXT_LEN)
    password = models.CharField(max_length = MAX_TEXT_LEN)
    count = models.IntegerField()
    
    @classmethod
    def login(cls, user, password):
        # Thank you based Django.
        try:
            user_obj = User.objects.get(user = user)
        except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
            return ERR_BAD_CREDENTIALS
        
        if user_obj.password != password:
            return ERR_BAD_CREDENTIALS
            
        user_obj.count += 1    
        user_obj.save()
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
            return ERR_USER_EXISTS
        # Username can't be empty. 
        if user == "" or len(user) > MAX_TEXT_LEN:
            return ERR_BAD_USERNAME
        
        if len(password) > MAX_TEXT_LEN:
            return ERR_BAD_PASSWORD
        
        new_user = User(user = user, password = password, count = 1)
        new_user.save()
        return SUCCESS
        
    @classmethod
    def TESTAPI_resetFixture(self):
        User.objects.all().delete()
        return SUCCESS