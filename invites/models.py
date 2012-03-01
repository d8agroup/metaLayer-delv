from django.contrib.auth.models import User
from django.db import models

class Invite(models.Model):
    user = models.ForeignKey(User, unique=True)
    code = models.TextField()
    to_email = models.EmailField()

