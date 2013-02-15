from django.db import models

# Create your models here.
SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

max_length = 128

class User(models.Model):
    user = models.CharField(max_length = max_length)
    password = models.CharField(max_length = max_length)
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
        if user == "" or len(user) > max_length:
            return ERR_BAD_USERNAME
        
        if len(password) > max_length:
            return ERR_BAD_PASSWORD
        
        new_user = User(user = user, password = password, count = 1)
        new_user.save()
        return SUCCESS
        
    @classmethod
    def TESTAPI_resetFixture(self):
        User.objects.all().delete()
        return SUCCESS





    
    
    
    
    