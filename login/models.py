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
    def add(self,user,password):
        if self.existingUsername(user)[0]:
            return ERR_USER_EXISTS
        if len(password) > max_length:
            return ERR_BAD_PASSWORD
        if user == "" or len(user) > max_length:
            return ERR_BAD_USERNAME
        newUser = User(userName=user, password = password,count=1)
        newUser.save()
        return SUCCESS

    @classmethod
    def login(self, user, password1):
        getUser = self.existingUsername(user)
        checkUser = getUser[1]
        checkPass = getUser[1].password
        checkCount = getUser[1].count
        if getUser[0] and checkPass == password1:
            checkCount+=1
            count = checkCount
            checkUser.save()
            return count
        else:
            return ERR_BAD_CREDENTIALS





    
    
    
    
    