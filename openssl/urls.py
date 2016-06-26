"""mapoint URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

from tastypie.api import Api

from apps.api import resource
from apps.api import views

api = Api(api_name=settings.TASTYPIE_API_VERSION)

api.register(resource.UserResource())
api.register(resource.DomainResource())
api.register(resource.CertificateResource())


urlpatterns = (
    url(r'^api/', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),

    # Common views
    url(r'^home$', TemplateView.as_view(template_name='common/home.html')),
    url(r'^verififaction$', TemplateView.as_view(
        template_name='common/verify.html')),
    url(r'^join$', TemplateView.as_view(template_name='common/register.html')),
    url(r'^signin$', TemplateView.as_view(template_name='common/login.html')),
    url(r'^certificate$', TemplateView.as_view(
        template_name='common/cert.html')),
    url(r'^reset$', TemplateView.as_view(
        template_name='common/reset.html')),
    url(r'^guide$', TemplateView.as_view(template_name='common/guide.html')),

    # Logged-in user
    url(r'^dashboard$', views.DashboardView.as_view()),
    url(r'^domains$', views.DomainsView.as_view()),
    url(r'^profile$', views.ProfileView.as_view()),
    url(r'^notification$', views.NotificationsView.as_view()),
    url(r'^stats$', views.LogsView.as_view()),

    # url(r'^blog', )

    url(r'^$', TemplateView.as_view(template_name='index.html')),
)


def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    template = loader.get_template('error/500.html')
    return HttpResponseServerError(template.render(Context({
        'request': request,
    })))
