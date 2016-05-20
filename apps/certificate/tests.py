from django.test import TestCase
from models import Certificate
from datetime import date, timedelta
import unittest


# Create your tests here.
class Certificate_Tests(TestCase):

    def setUp(self):
        self.mock = {
            "ssl_certificate": "thisisacertificate",
            "ssl_key": "thisisakey",
            "domain": "openssl.io",
            "date_registered": date.today() + timedelta(days=-10),
            "expiration_date": date.today() + timedelta(days=10),
            "last_updated": date.today() + timedelta(days=-5),
        }
        Certificate.objects.create(
            ssl_certificate=self.mock["ssl_certificate"],
            ssl_key=self.mock["ssl_key"],
            domain=self.mock["domain"],
            date_registered=self.mock["date_registered"],
            expiration_date=self.mock["expiration_date"],
            last_updated=self.mock["last_updated"],
        )

    def test_certificate_exists(self):
        certificate = Certificate.objects.latest('last_updated')
        self.assertIsInstance(certificate.id, int)

    def test_ssl_certificate(self):
        certificate = Certificate.objects.latest('date_registered')
        self.assertEquals(
            certificate.ssl_certificate, self.mock["ssl_certificate"])

    def test_certificate_can_be_updated(self):
        certificate = Certificate.objects.latest('last_updated')
        certificate.ssl_certificate = "Got a new cert"
        certificate.save()
        self.assertIsNotNone(Certificate.objects.filter(
            ssl_certificate="Got a new certificate"))

    def test_ssl_key(self):
        certificate = Certificate.objects.latest('last_updated')
        certificate_key = certificate.ssl_key
        self.assertIsNotNone(certificate_key)

    def test_domain_exists(self):
        certificate = Certificate.objects.latest('last_updated')
        certificate_domain = certificate.domain
        self.assertEquals(certificate_domain, "openssl.io")

    def test_date_registered(self):
        certificate = Certificate.objects.latest('last_updated')
        registered = certificate.date_registered
        self.assertEquals(registered, self.mock["date_registered"])

    def test_expiration_date(self):
        certificate = Certificate.objects.latest('last_updated')
        expiring = certificate.expiration_date
        self.assertEquals(expiring, self.mock["expiration_date"])

    def test_last_updated(self):
        certificate = Certificate.objects.latest('last_updated')
        updated = certificate.last_updated
        self.assertEquals(updated, self.mock["last_updated"])

if __name__ == '__main__':
    unittest()
