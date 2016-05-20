from django.test import TestCase
from models import Domain
from ..certificate.models import Certificate
from datetime import date, timedelta
import unittest


# Create your tests here.
class Domain_Tests(TestCase):

    def setUp(self):
        self.openssl_domain = Domain.objects.create(
            domain_name="openssl",
            domain_url="openssl.io",
            domain_registerer="Bernard Ojengwa",
            support_email="bernardojengwa@gmail.com",
            top_level_domain="google.com",
            domain_certificate=Certificate.objects.get(id=1),
            date_registered=date(2016, 1, 1),
            expiration_date=date(2017, 1, 1),
            last_updated=date.today() - timedelta(days=183),
            date_entered=date.today(),
        )
        self.openssl_domain.save()

    def test_domain_exists(self):
        domain = self.openssl_domain.objects.get(id=1)
        self.assertTrue(domain, int)

    def test_domain_name_availability(self):
        domain_name = self.openssl_domain.objects.get(name="domain_name")
        self.assertEqual(domain_name, "openssl")

    def test_domain_url_specificity(self):
        url = self.openssl_domain.objects.get(name="url")
        self.assertIs(url, "openssl.io")

    def test_support_email_is_an_email(self):
        email = self.openssl_domain.objects.get(name="support_email")
        mail = False
        for char in email:
            if char == "@":
                mail = True
            return mail
        self.assertIs(mail, True)

    def test_top_level_domain(self):
        tld = self.openssl_domain.objects.get(name="top_level_domain")
        self.assertNotEqual(tld, False)

    def domain_to_certificate_relationship(self):
        cert = self.openssl_domain.objects.get(pk=1)
        self.assertTrue(cert.openssl_certificate.ssl_key, "thisisakey")

    def test_date_registered(self):
        registered = self.openssl_domain.objects.get(name="date_registered")
        self.assertIs(registered, date(2016, 01, 01))

    def test_expiration(self):
        expiration = self.openssl_domain.objects.get(name="expiration_date")
        self.assertIs(expiration, date(2017, 01, 01))

    def test_last_updated(self):
        updated = self.openssl_domain.objects.get(name="last_updated")
        self.assertEqual(updated, date.today() - timedelta(days=183))

    def test_date_entered(self):
        entry = self.openssl_domain.objects.get(name="date_entered")
        self.assertEqual(entry, date.today())

if __name__ == '__main__':
    unittest()
