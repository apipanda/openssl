from datetime import datetime, timedelta

from django.db.models import signals

import tldextract
from tastypie.models import create_api_key

from django.contrib.auth.models import User
from app.models import Client
from workspace.models import (Organisation, OrganisationMember)


def add_to_org(sender, **kwargs):
    org = sender.objects.last()
    user = org.creator

    member, created = OrganisationMember.objects.get_or_create(
        org=org, member=user)

    if created:
        tld = tldextract.extract(org.url)

        client = Client()
        client.name = org.name
        client.organisation = org
        client.schema_name = org.slug
        client.paid_until = datetime.now() + timedelta(days=90)
        try:
            client.domain_url = tld.domain
            client.save()
        except KeyError:
            try:
                client.domain_url = tld.domain + '-' + tld.subdomain
                client.save()
            except KeyError:
                client.domain_url = org.slug
                client.save()

signals.post_save.connect(create_api_key, sender=User)
signals.post_save.connect(add_to_org, sender=Organisation)
