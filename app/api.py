from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from app.models import LocationModel


class LocationResource(ModelResource):
    class Meta:
        queryset = LocationModel.objects.all()
        resource_name = 'location'
        authorization = Authorization()
        authentication = Authentication()
