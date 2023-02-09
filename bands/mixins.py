from bands.models import Settings


LAST_VERSION_SETTING = 'last_data_version'

class UpdateDataVersionMixin(object):

    def save(self, *args, **kwargs):
        super(UpdateDataVersionMixin, self).save(*args, **kwargs)

        version, created = Settings.objects.get_or_create(key=LAST_VERSION_SETTING, defaults={'value':'1'})
        new_version = int(version.value) + 1
        version.value = new_version
        version.save()
