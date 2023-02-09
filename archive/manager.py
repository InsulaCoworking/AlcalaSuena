from django.db import models


class ArchivedManager(models.Manager):

    def current(self):
        return self.filter(archived=False)

    def archived(self, year):
        return self.filter(archived=True, archive_year=year)