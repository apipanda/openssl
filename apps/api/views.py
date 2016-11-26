from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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


class DashboardView(LoginRequiredView):
    template_name = "account/home.html"
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        kwargs.update({
                      'title': 'Dashboard'
                      })
        return super(DashboardView, self).get(self, request, *args, **kwargs)


class DomainsView(LoginRequiredView):
    template_name = "account/domains.html"
    http_method_names = ['get']


class ProfileView(LoginRequiredView):
    template_name = "account/profile.html"
    http_method_names = ['get']


class NotificationsView(LoginRequiredView):
    template_name = "account/notifications.html"
    http_method_names = ['get']


class LogsView(LoginRequiredView):
    template_name = "account/logs.html"
    http_method_names = ['get']


class EditView(LoginRequiredView):
    template_name = "account/edit.html"
    http_method_names = ['get']
