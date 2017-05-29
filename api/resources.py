from tastypie import fields
from tastypie.fields import IntegerField
from tastypie.resources import ModelResource

from bands.models import Band, Venue, Event, Tag, Settings


class TagResource(ModelResource):

    class Meta:
        queryset = Tag.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'tag'
        collection_name = 'tag'
        excludes = ['description']

class BandResource(ModelResource):
    tag = fields.ForeignKey(TagResource, 'tag', full=True, null=True)

    class Meta:
        queryset = Band.objects.all()
        list_allowed_methods = ['get']
        resource_name = 'bands'
        collection_name = 'bands'
        include_resource_uri = False

    # Remove the wrapper
    def alter_list_data_to_serialize(self, request, data):
        if self.Meta.collection_name in data and len(data[self.Meta.collection_name]) > 0:
            # only return the first result, avoid the "meta" field
            return data[self.Meta.collection_name]
        else:
            return []

class VenueResource(ModelResource):
    events = fields.ToManyField('api.resources.EventResource', 'venue', full=True, null=True)

    class Meta:
        queryset = Venue.objects.all()
        list_allowed_methods = ['get']
        resource_name = 'venues'
        collection_name = 'venues'
        include_resource_uri = False

    # Remove the wrapper
    def alter_list_data_to_serialize(self, request, data):
        if self.Meta.collection_name in data and len(data[self.Meta.collection_name]) > 0:
            # only return the first result, avoid the "meta" field
            return data[self.Meta.collection_name]
        else:
            return []

class EventResource(ModelResource):
    band = IntegerField(attribute="band__pk")

    class Meta:
        queryset = Event.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'events'
        collection_name = 'events'

class SettingsResource(ModelResource):
    class Meta:
        queryset = Settings.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'settings'
        collection_name = 'settings'

    def dehydrate(self, bundle):

        return bundle.data['value']