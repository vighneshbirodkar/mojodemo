from django.db import models

# Create your models here.

class MojoUser(models.Model):
    login = models.CharField(max_length=100)
    passwdHash = models.CharField(max_length=64)
    
    
