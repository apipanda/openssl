from __future__ import absolute_import
from django.contrib.auth.models import User
from django.utils.timezone import datetime, timedelta

from apps.certificate.models import Certificate
from apps.domain.models import Domain

import factory


class BaseUserFactory(factory.django.DjangoModelFactory):

    first_name = 'test'
    last_name = 'user'
    username = factory.Sequence(lambda n: "user%d" % n)
    date_joined = factory.LazyFunction(datetime.now)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    is_staff = False
    is_active = False

    class Meta:
        model = User
        django_get_or_create = ('email',)


class AnonymousUserFactory(BaseUserFactory):
    pass


class UserFactory(BaseUserFactory):
    is_active = True


class AdminFactory(BaseUserFactory):
    is_active = True
    is_staff = True


class CertificateFactory(factory.django.DjangoModelFactory):
    expiration_date = datetime.now() + timedelta(90)

    class Meta:
        model = Certificate


class DomainFactory(factory.django.DjangoModelFactory):
    date_registered = datetime.now()
    expiration_date = datetime.now() + timedelta(90)

    domain_certificate = factory.SubFactory(CertificateFactory)
    admin = factory.SubFactory(UserFactory)

    class Meta:
        model = Domain
