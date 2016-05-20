from __future__ import unicode_literals
from django.db import models
from ..certificate.models import Certificate


# Create your models here.
class Domain(models.Model):
    domain_name = models.CharField(max_length=200)
    domain_url = models.CharField(max_length=200)
    domain_registerer = models.CharField(max_length=200)
    support_email = models.CharField(max_length=200)
    top_level_domain = models.CharField(max_length=200)
    domain_certificate = models.OneToOneField(
        Certificate, related_name='certified_domain')
    date_registered = models.DateField()
    expiration_date = models.DateField()
    last_updated = models.DateField()
    date_entered = models.DateField(auto_now_add=True)

    def get_webmaster(self):
        pass

    def is_expired(self):
        if self.expiration_date > self.date_registered:
            return True
        else:
            return False
