from django_filters import FilterSet, AllValuesFilter
from .models import Comments
 
class PostFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
  
    def filter(self, queryset, value):
        return queryset
