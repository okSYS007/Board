from django_filters import FilterSet, AllValuesFilter
from .models import Comments
 
class PostFilter(FilterSet):

    # Announcement = AllValuesFilter(field_name='Announcement', method='filter_published')

    def filter_published(self, queryset, name, value):
        # construct the full lookup expression.
        lookup = '__'.join([name, 'isnull'])
        return queryset.filter(**{lookup: True})

        # alternatively, you could opt to hardcode the lookup. e.g.,
        # return queryset.filter(published_on__isnull=False)
    class Meta:
        model = Comments
        fields = ['Announcement']
