from django.db import models

from helpers.models import TimeStampedModel

# Create your models here.
class Pontiff(TimeStampedModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    papal_name = models.CharField(max_length=50)
    begin = models.DateField()
    finish = models.DateField()

    def __str__(self):
        return self.papal_name
