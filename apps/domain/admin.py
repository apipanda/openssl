from django.conf import settings

from django.contrib import admin
from models import Domain

# Register your models here.
class DomainAdmin(admin.ModelAdmin):
    '''
        Admin View for Domain
    '''
    date_hierarchy = 'expiration_date'
    actions_selection_counter = True
    empty_value_display = '-empty-'
    list_display = ('name', 'url', 'registrar', 'verification_type', 'owner')
    list_filter = ('is_active', 'verification_type')
    search_fields = ('name', 'url', 'owner')
    list_display_links = ('name',)


    def url(self, domain):
        return domain.domain_url

    def name(self, domain):
        return domain.domain_name

    def registrar(self, domain):
        return domain.domain_registrar

    def verification_type(self):
        verification_options = dict(settings.DOMAIN_VERIFICATION_OPTIONS)
        return verification_options[domain.verification_type]

    def owner(self, domain):
        return domain.admin.username

admin.site.register(Domain, DomainAdmin)