import whois
from datetime import datetime
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import (authenticate, login as
                                 django_login,
                                 logout as django_logout)

from django.contrib.auth.models import User

from tastypie import fields
from tastypie.cache import SimpleCache
from tastypie.http import (HttpForbidden, HttpNoContent,
                           HttpCreated, HttpAccepted)
from tastypie.utils import trailing_slash


from tastypie.resources import (ModelResource,)
from tastypie.validation import Validation
from tastypie.throttle import CacheDBThrottle
from tastypie.serializers import Serializer
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import (SessionAuthentication,
                                     MultiAuthentication,
                                     ApiKeyAuthentication)

from openssl.utils import json_serial
from apps.domain.models import Domain

from apps.api.exceptions import CustomBadRequest
from apps.certificate.models import Certificate


try:
    import json
except Exception:
    import simplejson as json

Authentication = MultiAuthentication(ApiKeyAuthentication(),
                                     SessionAuthentication(),)


class Resource(ModelResource):
    """docstring for Resource"""
    class Meta:

        always_return_data = True
        allowed_methods = ['get', 'post', 'put', 'patch', 'options', 'head']

        # authentication = Authentication
        # authorization = DjangoAuthorization()
        validation = Validation()
        collection_name = 'data'
        serializer = Serializer(formats=['json', 'jsonp'])
        cache = SimpleCache(timeout=10)
        throttle = CacheDBThrottle(throttle_at=settings.THROTTLE_TIMEOUT)


class DomainResource(Resource):
    webmaster = fields.ToOneField('apps.api.resource.UserResource', 'owner')

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/whois%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_whois'), name="whois"),
            # url(r'^(?P<resource_name>%s)/confim%s$' %
            #     (self._meta.resource_name, trailing_slash()),
            #     self.wrap_view('logout'), name='api_logout'),
        ]

    def get_whois(self, request, *args, **kwargs):
        self.method_check(request, ['post'])

        data = json.loads(request.body)
        host = data.get('host')

        try:
            domain = whois.whois(host)

            host = (lambda d: d.domain_name if isinstance(d.domain_name, str) else max(d.domain_name))(domain)

            expiration_date = (lambda d: d.expiration_date if isinstance(d.expiration_date, str) else min(d.expiration_date))(domain)

            if datetime.now() > expiration_date:
                resp = {
                    "success": False,
                    "status": 418,
                    "message": "Your Domain name has expired.",
                    "data": domain
                }
            else:
                resp = {
                    "success": True,
                    "message": "Whois record exist.",
                    "data": domain
                }

            return self.create_response(request, resp, HttpAccepted)

        except Exception, e:
            return CustomBadRequest(code='whois_error',
                                    message='Domain name verification error. Our developers have been notified.')

    class Meta(Resource.Meta):
        queryset = Domain.objects.filter(is_active=True)
        fields = ['id', 'domain_name', 'domain_url',
                  'slug', 'url', 'creator', 'owner']
        resource_name = 'domains'


class CertificateResource(Resource):
    class Meta(Resource.Meta):
        queryset = Certificate.objects.all()
        resource_name = 'certificates'


class UserResource(Resource):
    domains = fields.ToManyField(
        DomainResource, blank=True, null=True,
        full=True, use_in='detail',
        attribute=lambda bundle: Domain.objects
        .filter(creator=bundle.obj))

    class Meta(Resource.Meta):
        queryset = User.objects.all()
        fields = ['first_name', 'last_name',
                  'email', 'is_active', 'bills', 'orgs']
        resource_name = 'users'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def post_list(self, request, **kwargs):
        REQUIRED_REQUEST_FIELDS = (
            "email", "first_name", "domain", "password")

        bundle = json.loads(request.body)

        for field in REQUIRED_REQUEST_FIELDS:
            if field not in bundle:
                raise CustomBadRequest(
                    success=False,
                    code="missing_key",
                    message="Must provide %s when "
                    "creating a user." % field)

        REQUIRED_DOMAIN_FIELDS = ("name", "url", "domain_registrer")

        for field in REQUIRED_DOMAIN_FIELDS:
            if field not in bundle['org']:
                raise CustomBadRequest(
                    success=False,
                    code="missing_key",
                    message="Must provide %s when "
                    "creating an Domain." % field)

        try:
            email = bundle["email"]
            domain = bundle.pop('domain')

            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    success=False,
                    code="duplicate_exception",
                    message="That email address is already in used.")
            if Domain.objects.filter(domain_url=domain['url']):

                raise CustomBadRequest(
                    code="duplicate_exception",
                    message="The Domain you are "
                    "trying to create already exist.")

            user = User.objects.create_user(username=email, **bundle)
            user = authenticate(username=user.email,
                                password=bundle['password'])

            if user:
                django_login(request, user)

                domain.update(admin=user)

                Domain.objects.create(**domain)

                auth = request.COOKIES

                if user.is_active:
                    data = {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'last_login': user.last_login
                    }

                    resp = {
                        'success': True,
                        'message': 'User created successfully',
                        'data': data,
                        'auth': auth
                    }
                    return self.create_response(request, resp, HttpCreated)

        except KeyError:
            raise CustomBadRequest()

    def login(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get(
                                    'CONTENT_TYPE', 'application/json'))

        email = data.get('email', '')
        password = data.get('password', '')
        try:
            user = authenticate(username=email, password=password)
            if user:
                django_login(request, user)
                auth = request.COOKIES
                auth.update(apikey=user.api_key.key)
                if user.is_active:
                    data = {
                        'id': user.pk,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'last_login': user.last_login
                    }
                    resp = {
                        'success': True,
                        'message': 'Logged in successfully',
                        'data': data,
                        'auth': auth
                    }
                    return self.create_response(request, resp)
                else:
                    return self.create_response(request, {
                        'success': False,
                        'message': 'Your account have being suspended.',
                    }, HttpForbidden)
            else:
                raise CustomBadRequest(
                    code='invalid_entry',
                    message='Incorrect username/password combination.'
                )
        except KeyError:
            raise CustomBadRequest(
                code='invalid_entry',
                message='Incorrect username/password combination.'
            )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            django_logout(request)
            return self.create_response(request, {'success': True})
        else:
            raise CustomBadRequest(code='invalid_request',
                                   message="You are not logged in.")
