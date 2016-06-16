from __future__ import absolute_import

import unittest
from datetime import date, timedelta

from django.test import TestCase

from apps.domain.models import Domain
from apps.certificate.models import Certificate

from tests.fixtures.factories import (
    UserFactory, DomainFactory, CertificateFactory)


class Domain_Tests(TestCase):

    def setUp(self):

        self.user = UserFactory()

        self.certificate = CertificateFactory(**{
            "ssl_certificate": "thisisacertificate",
            "ssl_key": "thisisakey",
            "domain": "openssl.io",
            "date_registered": date.today() + timedelta(days=-10),
            "expiration_date": date.today() + timedelta(days=10),
            "last_updated": date.today() + timedelta(days=-5),
        })

        self.mock = {
            "domain_name": "openssl",
            "domain_url": "openssl.io",
            "domain_registerer": "Bernard Ojengwa",
            "support_email": "bernardojengwa@gmail.com",
            "tld": ".com",
            "domain_certificate": self.certificate,
            "expiration_date": date(2017, 1, 1),
            "last_updated": date.today(),
            "date_entered": date.today(),
            "admin": self.user
        }

        self.domain = DomainFactory(
            domain_name=self.mock["domain_name"],
            domain_url=self.mock["domain_url"],
            domain_registerer=self.mock["domain_registerer"],
            support_email=self.mock["support_email"],
            tld=self.mock["tld"],
            domain_certificate=self.mock["domain_certificate"],
            expiration_date=self.mock["expiration_date"],
            last_updated=self.mock["last_updated"],
            date_entered=self.mock["date_entered"],)

    def test_domain_exists(self):
        self.assertIsInstance(self.domain.id, int)

    def test_domain_name_availability(self):
        domain = Domain.objects.latest('date_entered')
        self.assertEquals(domain.domain_name, self.mock["domain_name"])

    def test_domain_url_specificity(self):
        domain = Domain.objects.latest('date_entered')
        self.assertEquals(domain.domain_url, self.mock["domain_url"])

    def test_support_email_is_an_email(self):
        domain = Domain.objects.latest('date_entered')
        email = domain.support_email
        self.assertIn("@", email)

    def test_tld(self):
        domain = Domain.objects.latest('date_entered')
        tld = domain.tld
        self.assertEquals(tld, self.mock["tld"])

    def domain_to_certificate_relationship(self):
        certificate = Certificate.objects.latest('last_updated')
        domain = Domain.objects.latest('date_entered')
        self.assertEqual(certificate, domain.certificate)

    def test_date_registered(self):
        registered = self.domain.date_registered
        self.assertEquals(registered, self.domain.date_registered)

    def test_expiration(self):
        domain = Domain.objects.latest('date_entered')
        self.assertEquals(domain.expiration_date, self.mock["expiration_date"])

    def test_last_updated(self):
        domain = Domain.objects.latest('date_entered')
        updated = domain.last_updated
        self.assertEquals(updated, self.mock["last_updated"])

    def test_date_entered(self):
        domain = Domain.objects.latest('date_entered')
        entry = domain.date_entered
        self.assertEquals(entry, self.mock["date_entered"])

    def test_url_can_be_updated(self):
        domain = Domain.objects.latest('date_entered')
        domain.domain_url = "bernardojengwa.com"
        domain.save()
        self.assertEquals(domain.domain_url, "bernardojengwa.com")

if __name__ == '__main__':
    unittest.main()
