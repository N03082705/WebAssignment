from django.db import models

class TempReading(models.Model):
    reading = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)