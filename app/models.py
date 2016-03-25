from __future__ import unicode_literals

from django.db import models

# Create your models here.


class LocationModel(models.Model):

    address = models.CharField(blank=False, null=False, max_length=255)
    longitude = models.CharField(max_length=15)
    latitude = models.CharField(max_length=15)
    place_id = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "location"
        verbose_name_plural = "locations"
        unique_together = (('longitude', 'latitude'),)

    def __str__(self):
        return "{0}:{1}".format(self.pk, self.name)

    def ___unicode__(self):
        return "{0}:{1}".format(self.pk, self.name)
