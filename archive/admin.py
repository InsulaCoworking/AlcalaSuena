# coding=utf-8

# Register your models here.
from django.contrib.admin import SimpleListFilter


class ArchiveFilter(SimpleListFilter):
  title = 'Archivada' # a label for our filter
  parameter_name = 'archive' # you can put anything here

  def lookups(self, request, model_admin):
    # This is where you create filter options; we have two:
    return [
        ('archived', 'Archivadas'),
        ('not_archived', 'No archivadas'),
    ]

  def queryset(self, request, queryset):
    # This is where you process parameters selected by use via filter options:
    if self.value() == 'archived':
        # Get websites that have at least one page.
      return queryset.distinct().filter(archived=True)

    if self.value():
        # Get websites that don't have any pages.
        return queryset.distinct().filter(archived=False)
