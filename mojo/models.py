from django.db import models

# Create your models here.

class MojoUser(models.Model):
    login = models.CharField(max_length=100,primary_key = True)
    passwdHash = models.CharField(max_length=64)
    # The token from instamojo API
    mojoToken = models.CharField(max_length=100)

    
