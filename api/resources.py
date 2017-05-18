from tastypie.resources import ModelResource

from bands.models import Band


class BandResource(ModelResource):

    class Meta:
        queryset = Band.objects.all()
        list_allowed_methods = ['get']
        resource_name = 'bands'
        collection_name = 'bands'
        include_resource_uri = False