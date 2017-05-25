from tastypie.api import Api

from api.resources import BandResource, VenueResource, EventResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(BandResource())
    api.register(VenueResource())
    api.register(EventResource())

    return api