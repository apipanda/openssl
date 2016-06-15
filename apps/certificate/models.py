from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Certificate(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    ssl_certificate = models.CharField(max_length=200)
    ssl_key = models.CharField(max_length=200)
    domain = models.CharField(max_length=200)
    date_registered = models.DateField(auto_now=True)
    expiration_date = models.DateField()
    last_updated = models.DateField(auto_now_add=True)
