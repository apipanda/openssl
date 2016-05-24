from django.test import TestCase
from models import Domain
from ..certificate.models import Certificate
# from ..certificate.tests import Certificate_Tests
from datetime import date, timedelta
import unittest


# Create your tests here.
class Domain_Tests(TestCase):
    # Certificate_Tests()

    def setUp(self):
        Certificate.objects.create(**{
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
            "top_level_domain": "google.com",
            "domain_certificate": Certificate.objects.latest('last_updated'),
            "date_registered": date(2016, 1, 1),
            "expiration_date": date(2017, 1, 1),
            "last_updated": date.today() - timedelta(days=183),
            "date_entered": date.today(),
        }

        Domain.objects.create(
            domain_name=self.mock["domain_name"],
            domain_url=self.mock["domain_url"],
            domain_registerer=self.mock["domain_registerer"],
            support_email=self.mock["support_email"],
            top_level_domain=self.mock["top_level_domain"],
            domain_certificate=self.mock["domain_certificate"],
            date_registered=self.mock["date_registered"],
            expiration_date=self.mock["expiration_date"],
            last_updated=self.mock["last_updated"],
            date_entered=self.mock["date_entered"],
        )

    def test_domain_exists(self):
        domain = Domain.objects.latest('date_entered')
        self.assertIsInstance(domain.id, int)

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

    def test_top_level_domain(self):
        domain = Domain.objects.latest('date_entered')
        tld = domain.top_level_domain
        self.assertEquals(tld, self.mock["top_level_domain"])

    def domain_to_certificate_relationship(self):
        certificate = Certificate.objects.latest('last_updated')
        domain = Domain.objects.latest('date_entered')
        self.assertEqual(certificate, domain.certificate)

    def test_date_registered(self):
        domain = Domain.objects.latest('date_entered')
        registered = domain.date_registered
        self.assertEquals(registered, self.mock["date_registered"])

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
