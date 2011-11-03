from django.db import models

class CacheEntry(models.Model):
    key = models.CharField(max_length=255, unique=True)
    cache = models.TextField()
    time = models.IntegerField()
    
class RegisteredEmail(models.Model):
    email = models.CharField(max_length=255, unique=True)
    approved = models.BooleanField()
    
    
