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
    def __unicode__(self):
        return str((self.user, self.password, self.count))
    
    @classmethod
    def TESTAPI_resetFixture(self):
        User.objects.all().delete()
        return SUCCESS
    
    @classmethod
    def existingUsername(self,user):
        try:
            user1 = User.objects.get(user = user)
            Exist = True
        except:
            Exist=False
            user1 = ""
        return (Exist,user1)
    
    @classmethod
    def add(self,user1,pass1):
        if self.existingUsername(user1)[0]:
            return ERR_USER_EXISTS
        if user1 == "" or len(user1) > 128:
            return ERR_BAD_USERNAME
        if len(pass1) > 128:
            return ERR_BAD_PASSWORD
        add1 = User(user=user1, password = pass1, count=1)
        add1.save()
        return SUCCESS
    
    @classmethod
    def login(self, user2, pass2):
        login1 = self.existingUsername(user2)
        if login1[0] and login1[1].password == pass2:
            login1[1].count+=1
            count1 = login1[1].count
            login1[1].save()
            return count1
        else:
            return ERR_BAD_CREDENTIALS
    
