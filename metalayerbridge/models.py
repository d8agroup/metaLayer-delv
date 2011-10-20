from django.db import models

class SentimentCache(models.Model):
    text_hash = models.CharField(max_length=255, unique=True)
    sentiment = models.DecimalField(decimal_places=10, max_digits=12)
    
