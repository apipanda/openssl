from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

# Create your views here.


class BaseView(TemplateView):

    def dispatch(self, request, *args, **kwargs):

        if not request.is_ajax():
            return HttpResponseRedirect(reverse('index'))

        return super(BaseView, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class LoginRequiredView(BaseView):

    def get(self, request, *args, **kwargs):

        return super(LoginRequiredView, self).get(self, request, *args, **kwargs)


class DashView(LoginRequiredView):
    template_name = "account/home.html"
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        kwargs.update({
                      'title': 'Dashboard'
                      })
        return super(DashView, self).get(self, request, *args, **kwargs)


class SwitcherView(LoginRequiredView):
    template_name = "account/switcher.html"
    http_method_names = ['get']


class HubView(LoginRequiredView):
    template_name = "account/hubs.html"
    http_method_names = ['get']


class OrgView(LoginRequiredView):
    template_name = "account/orgs.html"
    http_method_names = ['get']


class WorkspaceView(LoginRequiredView):
    template_name = "account/workspace.html"
    http_method_names = ['get']


class PluginView(LoginRequiredView):
    template_name = "account/plugins.html"
    http_method_names = ['get']


class ProfileView(LoginRequiredView):
    template_name = "account/profile.html"
    http_method_names = ['get']
