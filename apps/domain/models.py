from __future__ import unicode_literals, absolute_import
from django.contrib.auth.models import User
from django.db import models
from apps.certificate.models import Certificate


# Create your models here.
class Domain(models.Model):
    domain_name = models.CharField(max_length=200)
    domain_url = models.CharField(max_length=200)
    domain_registerer = models.CharField(max_length=200)
    support_email = models.EmailField(max_length=200)
    tld = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    date_registered = models.DateField()
    expiration_date = models.DateField()
    last_updated = models.DateField(auto_now=True)
    date_entered = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    domain_certificate = models.ForeignKey(
        Certificate, related_name='certified_domain')
    admin = models.ForeignKey(User, related_name='domains')

    def get_webmaster(self):
        return self.admin

    @property
    def is_expired(self):
        return True if self.expiration_date > self.date_registered else False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = (self.domain_name + self.tld).replace('.', '-')
        return super(Domain, self).save(*args, **kwargs)
