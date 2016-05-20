from django.test import TestCase
from models import Certificate
from datetime import date, timedelta
import unittest


# Create your tests here.
class Certificate_Tests(TestCase):

    def setUp(self):
        self.openssl_certificate = Certificate.objects.create(
            ssl_certificate="thisisacertificate",
            ssl_key="thisisakey",
            domain="openssl.io",
            date_registered=date.today() + timedelta(days=-10),
            expiration_date=date.today() + timedelta(days=10),
            last_updated=date.today() + timedelta(days=-5)
        )
        self.openssl_certificate.save()

    def test_certificate_exists(self):
        certificate_id = self.openssl_certificate.objects.get(id)
        self.assertTrue(certificate_id, int)

    def test_ssl_certificate(self):
        certificate = self.openssl_certificate.objects.get(
            name="ssl_certificate")
        self.assertTrue(certificate, str)

    def test_ssl_key(self):
        certificate_key = self.openssl_certificate.objects.get(name="ssl_key")
        self.assertTrue(certificate_key, str)

    def test_domain_exists(self):
        domain = self.openssl_certificate.objects.get(name="domain")
        self.assertEqual(domain, "openssl.io")

    def test_date_resigtered(self):
        registered = self.openssl_certificate.objects.get(
            name="date_registered")
        self.assertIs(registered, date(2016, 04, 14))

    def test_expiration_date(self):
        expiring = self.openssl_certificate.objects.get(name="expiration")
        self.asserIs(expiring, date(2017, 04, 14))

    def test_last_updated(self):
        updated = self.openssl_certificate.objects.get(name="last_updated")
        self.assertEqual(updated, date.today())

if __name__ == '__main__':
    unittest()
